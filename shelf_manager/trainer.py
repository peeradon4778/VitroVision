"""Training logic — เรียกจาก main.py (VitroShelf)"""
import sqlite3, threading, json, random, base64, io, time as _time
import cv2
from PIL import Image as _PIL
from collections import Counter
from pathlib import Path

# timm, torch, albumentations โหลดเฉพาะตอนเริ่ม train/preview จริง
# (ประหยัด ~9s จาก startup time)
_heavy_loaded = False

def _ensure_heavy():
    global _heavy_loaded, torch, nn, timm, A, ToTensorV2
    global Dataset, DataLoader, CosineAnnealingLR
    global train_test_split, confusion_matrix, classification_report
    global cohen_kappa_score, f1_score
    if _heavy_loaded:
        return
    import torch as _torch, torch.nn as _nn
    import timm as _timm
    import albumentations as _A
    from albumentations.pytorch import ToTensorV2 as _T2
    from torch.utils.data import Dataset as _DS, DataLoader as _DL
    from torch.optim.lr_scheduler import CosineAnnealingLR as _CA
    from sklearn.model_selection import train_test_split as _tts
    from sklearn.metrics import (confusion_matrix as _cm,
                                  classification_report as _cr,
                                  cohen_kappa_score as _cks,
                                  f1_score as _f1)
    torch = _torch; nn = _nn; timm = _timm; A = _A; ToTensorV2 = _T2
    Dataset = _DS; DataLoader = _DL; CosineAnnealingLR = _CA
    train_test_split = _tts
    confusion_matrix = _cm; classification_report = _cr
    cohen_kappa_score = _cks; f1_score = _f1
    _heavy_loaded = True

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
        if not path:
            continue
        p = Path(path) if Path(path).is_absolute() else Path(base_dir) / path
        if p.exists() and p.is_file():
            valid.append(status)
    counts = Counter(valid)
    return {
        'total': len(valid),
        'per_class': {cls: counts.get(cls, 0) for cls in LABELS},
        'ready': len(valid) >= 6,
    }


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
    _ensure_heavy()
    _stop.clear()

    class _DS(Dataset):
        def __init__(self, paths, labels, aug):
            self.paths  = paths
            self.labels = [L2I[l] for l in labels]
            self.aug    = aug
        def __len__(self): return len(self.paths)
        def __getitem__(self, idx):
            # paths ผ่าน pre-validate decode มาแล้ว แต่กันสองชั้น เผื่อไฟล์เสียระหว่าง train
            # ถ้า decode ไม่ได้ ให้ข้ามไปหยิบ sample ถัดไป — ไม่ฉีดภาพดำเข้า training
            for _ in range(len(self.paths)):
                raw = cv2.imread(self.paths[idx])
                if raw is not None:
                    img = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)
                    return self.aug(image=img)['image'], self.labels[idx]
                idx = (idx + 1) % len(self.paths)
            raise RuntimeError('อ่านภาพไม่ได้เลยสักไฟล์ใน dataset')

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
    n_skipped = 0
    for path, status in rows:
        if not path:
            continue
        p = Path(path) if Path(path).is_absolute() else Path(base_dir) / path
        # exists() ไม่พอ — ต้องลอง decode จริง เพราะไฟล์อาจเสีย/เขียนไม่จบ/ไม่ใช่ภาพ
        # ทำให้ cv2.imread คืน None แล้ว cvtColor ใน __getitem__ จะ crash กลาง DataLoader
        if p.exists() and p.is_file():
            if cv2.imread(str(p)) is None:
                n_skipped += 1
                continue
            paths.append(str(p)); labels.append(status)

    if n_skipped:
        on_log({'type': 'log',
                'msg': f'ข้ามภาพที่ decode ไม่ได้ {n_skipped} ภาพ (เสีย/ไม่ใช่ภาพ/เขียนไม่จบ)'})

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

    # ── Weights & Biases (optional) ───────────────────────────────
    _wb_run = None
    try:
        import wandb as _wandb
        _wb_run = _wandb.init(
            project='vitrovision',
            config={
                'model': 'efficientnet_b0',
                'epochs_head': ep_head, 'epochs_full': ep_full,
                'lr': lr, 'img_size': IMG_SIZE, 'batch_size': 8,
                'n_train': len(tr_p), 'n_val': len(vl_p), 'n_test': len(te_p),
                'class_weights': {cls: round(class_weights[i].item(), 3)
                                  for i, cls in enumerate(LABELS)},
            },
            reinit=True, tags=['capsicum', 'tc-monitoring'],
        )
        on_log({'type': 'log', 'msg': f'wandb: {_wb_run.url}'})
    except Exception as _e:
        on_log({'type': 'log', 'msg': f'wandb ไม่พร้อม — เทรนต่อโดยไม่มี wandb ({_e})'})

    # ── Augmentation ─────────────────────────────────────────────
    mean, std = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]
    tr_aug = A.Compose([
        A.RandomResizedCrop(size=(IMG_SIZE, IMG_SIZE), scale=(0.65, 1.0)),
        A.HorizontalFlip(p=0.5), A.VerticalFlip(p=0.3), A.RandomRotate90(p=0.5),
        A.ColorJitter(0.35, 0.35, 0.3, 0.08, p=0.8),
        A.GaussianBlur(blur_limit=(3, 7), p=0.3),
        A.GaussNoise(p=0.3),
        A.Normalize(mean=mean, std=std), ToTensorV2(),
    ])
    vl_aug = A.Compose([A.Resize(IMG_SIZE, IMG_SIZE),
                        A.Normalize(mean=mean, std=std), ToTensorV2()])

    tr_loader = DataLoader(_DS(tr_p, tr_l, tr_aug), batch_size=8, shuffle=True,  num_workers=0)
    vl_loader = DataLoader(_DS(vl_p, vl_l, vl_aug), batch_size=8, shuffle=False, num_workers=0)
    te_loader = DataLoader(_DS(te_p, te_l, vl_aug), batch_size=8, shuffle=False, num_workers=0)

    model     = timm.create_model('efficientnet_b0', pretrained=True, num_classes=3)
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    ckpt_dir  = Path(model_out).parent.parent / 'checkpoints'
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    best_loss = float('inf')

    def epoch_loop(loader, opt=None):
        model.train() if opt else model.eval()
        tot_loss = correct = n = 0
        ctx = torch.enable_grad() if opt else torch.no_grad()
        with ctx:
            for imgs, tgts in loader:
                out  = model(imgs)
                loss = criterion(out, tgts)
                if opt: opt.zero_grad(); loss.backward(); opt.step()
                tot_loss += loss.item() * len(tgts)
                correct  += (out.argmax(1) == tgts).sum().item()
                n        += len(tgts)
        return tot_loss / n, correct / n

    def phase(phase_num, total_ep, opt, scheduler):
        nonlocal best_loss
        on_log({'type': 'phase', 'phase': phase_num, 'total': total_ep,
                'n_train': len(tr_p)})
        ep_times = []
        for ep in range(1, total_ep + 1):
            if _stop.is_set():
                on_log({'type': 'log', 'msg': 'หยุดโดยผู้ใช้'})
                on_log({'type': 'error', 'msg': 'หยุดโดยผู้ใช้ — กด Train ใหม่เพื่อเริ่มใหม่'})
                return False
            t0 = _time.time()
            tl, ta = epoch_loop(tr_loader, opt)
            vl, va = epoch_loop(vl_loader)
            scheduler.step()
            duration = _time.time() - t0
            ep_times.append(duration)
            avg_t   = sum(ep_times[-5:]) / min(len(ep_times), 5)
            eta_sec = int(avg_t * (total_ep - ep))
            current_lr = opt.param_groups[0]['lr']
            if vl < best_loss:
                best_loss = vl
                torch.save(model, ckpt_dir / 'best.pt')
            on_log({'type': 'epoch', 'phase': phase_num, 'epoch': ep, 'total': total_ep,
                    'tl': round(tl, 4), 'vl': round(vl, 4),
                    'ta': round(ta * 100, 1), 'va': round(va * 100, 1),
                    'lr': round(current_lr, 7),
                    'duration': round(duration, 1),
                    'eta_sec': eta_sec,
                    'imgs_done': ep * len(tr_p)})
            if _wb_run:
                _wb_run.log({
                    'train/loss': tl, 'train/acc': ta * 100,
                    'val/loss': vl,   'val/acc':   va * 100,
                    'lr': current_lr, 'phase': phase_num,
                })
        return True

    # Phase 1 — head only (lr → lr*0.01 แบบ cosine)
    for p in model.parameters(): p.requires_grad = False
    for p in model.classifier.parameters(): p.requires_grad = True
    opt1 = torch.optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()), lr=lr)
    sch1 = CosineAnnealingLR(opt1, T_max=ep_head, eta_min=lr * 0.01)
    if not phase(1, ep_head, opt1, sch1):
        return

    # Phase 2 — fine-tune all (lr*0.1 → lr*0.001 แบบ cosine)
    for p in model.parameters(): p.requires_grad = True
    opt2 = torch.optim.Adam(model.parameters(), lr=lr * 0.1)
    sch2 = CosineAnnealingLR(opt2, T_max=ep_full, eta_min=lr * 0.001)
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

    if _wb_run:
        try:
            import wandb as _wandb
            _wb_run.log({
                'test/kappa':       kappa,
                'test/weighted_f1': wf1,
                'test/confusion_matrix': _wandb.plot.confusion_matrix(
                    probs=None, y_true=trues, preds=preds, class_names=LABELS),
                **{f'test/{cls}/recall':    report[cls]['recall']    for cls in LABELS},
                **{f'test/{cls}/f1':        report[cls]['f1-score']  for cls in LABELS},
                **{f'test/{cls}/precision': report[cls]['precision'] for cls in LABELS},
            })
            _wb_run.finish()
        except Exception:
            pass


def get_preview(db_path, base_dir, n=8):
    """คืน list ของ {original, augmented, label} เป็น base64 JPEG"""
    _ensure_heavy()
    conn = sqlite3.connect(str(db_path))
    rows = conn.execute(
        "SELECT local_path, status FROM images "
        "WHERE status IN ('healthy','contaminated','dead')"
    ).fetchall()
    conn.close()

    valid = []
    for path, status in rows:
        p = Path(path) if Path(path).is_absolute() else Path(base_dir) / path
        if p.exists():
            valid.append((str(p), status))

    if not valid:
        return []

    aug = A.Compose([
        A.RandomResizedCrop(size=(IMG_SIZE, IMG_SIZE), scale=(0.65, 1.0)),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.3),
        A.RandomRotate90(p=0.5),
        A.ColorJitter(0.35, 0.35, 0.3, 0.08, p=0.8),
        A.GaussianBlur(blur_limit=(3, 7), p=0.3),
        A.GaussNoise(p=0.3),
    ])

    def _b64(arr):
        pil = _PIL.fromarray(arr)
        buf = io.BytesIO()
        pil.save(buf, format='JPEG', quality=82)
        return base64.b64encode(buf.getvalue()).decode()

    results = []
    for path, status in random.sample(valid, min(n, len(valid))):
        # อ่านก่อน เช็ค None ก่อน แล้วค่อย cvtColor — กัน cv2.imread คืน None แล้ว crash
        raw = cv2.imread(path)
        if raw is None:
            continue
        img     = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)
        orig    = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        aug_img = aug(image=img)['image']
        results.append({
            'original':  _b64(orig),
            'augmented': _b64(aug_img),
            'label':     status,
        })
    return results
