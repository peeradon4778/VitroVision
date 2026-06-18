"""Training logic — เรียกจาก main.py (VitroShelf)"""
import sqlite3, threading, json
import cv2, torch, torch.nn as nn, torch.nn.functional as F
import timm
from timm.data.mixup import Mixup
from .transforms import get_train_transforms, get_val_transforms
from torch.utils.data import Dataset, DataLoader
from torch.optim.lr_scheduler import CosineAnnealingLR
from sklearn.model_selection import train_test_split
from sklearn.metrics import (confusion_matrix, classification_report,
                              cohen_kappa_score, f1_score)
from collections import Counter
from pathlib import Path

LABELS   = ['healthy', 'contaminated', 'dead']
L2I      = {l: i for i, l in enumerate(LABELS)}
IMG_SIZE = 224
_stop    = threading.Event()


def stop():
    _stop.set()


def get_stats(db_path, base_dir):
    try:
        conn = sqlite3.connect(str(db_path))
        rows = conn.execute(
            "SELECT local_path, status FROM images "
            "WHERE status IN ('healthy','contaminated','dead')"
        ).fetchall()
        conn.close()
    except Exception:
        rows = []
    valid = []
    for path, status in rows:
        p = Path(path) if Path(path).is_absolute() else Path(base_dir) / path
        if p.exists():
            valid.append(status)
    counts = Counter(valid)
    return {
        'total': len(valid),
        'per_class': {cls: counts.get(cls, 0) for cls in LABELS},
        'ready': len(valid) >= 6,
    }


class _DS(Dataset):
    def __init__(self, paths, labels, aug):
        self.paths  = paths
        self.labels = [L2I[l] for l in labels]
        self.aug    = aug

    def __len__(self): return len(self.paths)

    def __getitem__(self, idx):
        img = cv2.cvtColor(cv2.imread(self.paths[idx]), cv2.COLOR_BGR2RGB)
        return self.aug(image=img)['image'], self.labels[idx]


def _evaluate(model, loader):
    """Run model on DataLoader → (preds, trues) as int lists"""
    model.eval()
    preds, trues = [], []
    with torch.no_grad():
        for imgs, tgts in loader:
            preds.extend(model(imgs).argmax(1).tolist())
            trues.extend(tgts.tolist())
    return preds, trues


def run_training(db_path, base_dir, model_out, cfg, on_log):
    _stop.clear()
    ep_head = cfg.get('epochs_head', 15)
    ep_full = cfg.get('epochs_full', 25)
    lr      = cfg.get('lr', 1e-4)

    # โหลด paths จาก DB
    conn = sqlite3.connect(str(db_path))
    rows = conn.execute(
        "SELECT local_path, status FROM images "
        "WHERE status IN ('healthy','contaminated','dead')"
    ).fetchall()
    conn.close()

    paths, labels = [], []
    for path, status in rows:
        p = Path(path) if Path(path).is_absolute() else Path(base_dir) / path
        if p.exists():
            paths.append(str(p)); labels.append(status)

    if len(paths) < 6:
        on_log({'type': 'error', 'msg': f'ภาพน้อยเกินไป ({len(paths)}) — ต้องการอย่างน้อย 6'}); return

    on_log({'type': 'log', 'msg': f'ภาพทั้งหมด {len(paths)}: {dict(Counter(labels))}'})

    # ── Train / Val / Test Split ─────────────────────────────────
    min_c    = min(Counter(labels).values())
    use_test = len(paths) >= 30

    try:
        if use_test:
            tr_p, tmp_p, tr_l, tmp_l = train_test_split(
                paths, labels, test_size=0.30,
                stratify=labels if min_c >= 3 else None, random_state=42)
            min_c2 = min(Counter(tmp_l).values())
            vl_p, te_p, vl_l, te_l = train_test_split(
                tmp_p, tmp_l, test_size=0.50,
                stratify=tmp_l if min_c2 >= 2 else None, random_state=42)
            on_log({'type': 'log',
                    'msg': f'Split 70/15/15 — Train {len(tr_p)} | Val {len(vl_p)} | Test {len(te_p)}'})
        else:
            tr_p, vl_p, tr_l, vl_l = train_test_split(
                paths, labels, test_size=0.2,
                stratify=labels if min_c >= 3 else None, random_state=42)
            te_p, te_l = vl_p, vl_l
            on_log({'type': 'log',
                    'msg': f'Split 80/20 — Train {len(tr_p)} | Val {len(vl_p)} '
                           f'(ใช้ val แทน test — ต้องการ ≥30 ภาพสำหรับ test set แยก)'})
    except ValueError:
        tr_p, vl_p, tr_l, vl_l = (paths, paths[:max(1, len(paths)//5)],
                                   labels, labels[:max(1, len(labels)//5)])
        te_p, te_l = vl_p, vl_l

    # ── Class Weights (แก้ปัญหา imbalanced dataset) ─────────────
    tr_counter = Counter(tr_l)
    n_train    = len(tr_l)
    class_weights = torch.tensor([
        n_train / (len(LABELS) * max(tr_counter.get(cls, 1), 1))
        for cls in LABELS
    ], dtype=torch.float)
    w_info = '  |  '.join(
        f'{cls}: {class_weights[i]:.3f}' for i, cls in enumerate(LABELS)
    )
    on_log({'type': 'log', 'msg': f'Class weights — {w_info}'})
    on_log({'type': 'weights', 'weights': {
        cls: round(class_weights[i].item(), 3) for i, cls in enumerate(LABELS)
    }})

    # ── Augmentation ─────────────────────────────────────────────
    tr_aug = get_train_transforms(size=IMG_SIZE)
    vl_aug = get_val_transforms(size=IMG_SIZE)

    tr_loader = DataLoader(_DS(tr_p, tr_l, tr_aug), batch_size=8, shuffle=True,  num_workers=0)
    vl_loader = DataLoader(_DS(vl_p, vl_l, vl_aug), batch_size=8, shuffle=False, num_workers=0)
    te_loader = DataLoader(_DS(te_p, te_l, vl_aug), batch_size=8, shuffle=False, num_workers=0)

    model     = timm.create_model('vit_small_patch14_dinov2', pretrained=True,
                                   num_classes=3, img_size=224)
    criterion = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=0.1)
    mixup_fn  = Mixup(mixup_alpha=0.2, cutmix_alpha=0.0,
                      label_smoothing=0.1, num_classes=3)
    ckpt_dir  = Path(model_out).parent.parent / 'checkpoints'
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    best_loss = float('inf')

    def epoch_loop(loader, opt=None):
        model.train() if opt else model.eval()
        tot_loss = correct = n = 0
        ctx = torch.enable_grad() if opt else torch.no_grad()
        with ctx:
            for imgs, tgts in loader:
                if opt:
                    imgs, soft = mixup_fn(imgs, tgts)
                    out  = model(imgs)
                    loss = F.cross_entropy(out, soft)
                    correct += (out.argmax(1) == soft.argmax(1)).sum().item()
                else:
                    out  = model(imgs)
                    loss = criterion(out, tgts)
                    correct += (out.argmax(1) == tgts).sum().item()
                if opt: opt.zero_grad(); loss.backward(); opt.step()
                tot_loss += loss.item() * len(tgts)
                n        += len(tgts)
        return tot_loss / n, correct / n

    def phase(phase_num, total_ep, opt, scheduler):
        nonlocal best_loss
        on_log({'type': 'phase', 'phase': phase_num, 'total': total_ep})
        for ep in range(1, total_ep + 1):
            if _stop.is_set():
                on_log({'type': 'log', 'msg': 'หยุดโดยผู้ใช้'}); return False
            tl, ta = epoch_loop(tr_loader, opt)
            vl, va = epoch_loop(vl_loader)
            scheduler.step()
            current_lr = opt.param_groups[0]['lr']
            if vl < best_loss:
                best_loss = vl
                torch.save(model, ckpt_dir / 'best.pt')
            on_log({'type': 'epoch', 'phase': phase_num, 'epoch': ep, 'total': total_ep,
                    'tl': round(tl, 4), 'vl': round(vl, 4),
                    'ta': round(ta * 100, 1), 'va': round(va * 100, 1),
                    'lr': round(current_lr, 7)})
        return True

    # Phase 1 — head only (lr → lr*0.01 แบบ cosine)
    for p in model.parameters(): p.requires_grad = False
    for p in model.head.parameters(): p.requires_grad = True
    opt1 = torch.optim.AdamW(model.head.parameters(), lr=lr, weight_decay=1e-2)
    sch1 = CosineAnnealingLR(opt1, T_max=ep_head, eta_min=lr * 0.01)
    if not phase(1, ep_head, opt1, sch1):
        return

    # Phase 2 — fine-tune all (lr*0.1 → lr*0.001 แบบ cosine)
    for p in model.parameters(): p.requires_grad = True
    opt2 = torch.optim.AdamW([
        {'params': [p for n, p in model.named_parameters() if 'head' not in n], 'lr': 1e-5},
        {'params': model.head.parameters(), 'lr': 1e-4},
    ], weight_decay=1e-2)
    sch2 = CosineAnnealingLR(opt2, T_max=ep_full, eta_min=1e-7)
    if not phase(2, ep_full, opt2, sch2):
        return

    # บันทึก final model
    best = ckpt_dir / 'best.pt'
    final_model = torch.load(str(best), map_location='cpu', weights_only=False) if best.exists() else model
    Path(model_out).parent.mkdir(parents=True, exist_ok=True)
    torch.save(final_model, model_out)
    on_log({'type': 'log', 'msg': 'บันทึก model แล้ว — กำลังประเมินผลบน Test Set...'})

    # ── Evaluation ───────────────────────────────────────────────
    preds, trues = _evaluate(final_model, te_loader)

    cm     = confusion_matrix(trues, preds, labels=list(range(3)))
    report = classification_report(trues, preds, target_names=LABELS,
                                   output_dict=True, zero_division=0)
    kappa  = cohen_kappa_score(trues, preds) if len(set(trues)) > 1 else 0.0
    wf1    = f1_score(trues, preds, average='weighted', zero_division=0)

    on_log({
        'type':        'confusion',
        'matrix':      cm.tolist(),
        'labels':      LABELS,
        'kappa':       round(kappa, 4),
        'weighted_f1': round(wf1, 4),
        'test_n':      len(te_p),
        'is_test':     use_test,
    })
    for cls in LABELS:
        r = report[cls]
        on_log({
            'type':      'class_metric',
            'label':     cls,
            'precision': round(r['precision'], 3),
            'recall':    round(r['recall'],    3),
            'f1':        round(r['f1-score'],  3),
            'support':   int(r['support']),
        })

    # บันทึก metrics.json
    metrics_path = Path(model_out).parent / 'metrics.json'
    with open(str(metrics_path), 'w', encoding='utf-8') as f:
        json.dump({
            'confusion_matrix':      cm.tolist(),
            'labels':                LABELS,
            'classification_report': {k: v for k, v in report.items()
                                      if k != 'accuracy'},
            'cohen_kappa':           round(kappa, 4),
            'weighted_f1':           round(wf1, 4),
            'class_weights':         {cls: round(class_weights[i].item(), 3)
                                      for i, cls in enumerate(LABELS)},
            'n_train': len(tr_p), 'n_val': len(vl_p), 'n_test': len(te_p),
            'is_separate_test': use_test,
        }, f, ensure_ascii=False, indent=2)

    on_log({'type': 'done',
            'msg':  f'เสร็จสมบูรณ์ — Weighted F1: {wf1:.3f} | Cohen\'s κ: {kappa:.3f}'})
