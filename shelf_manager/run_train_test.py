"""Training pipeline test"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from pathlib import Path
import trainer

DB_PATH  = Path('vitroshelf.db')
BASE_DIR = Path('.')
MODEL_OUT = Path('../models/final/classifier.pt')

cfg = {
    'epochs_head': 3,
    'epochs_full': 5,
    'lr': 1e-4,
}

def on_log(data):
    t = data.get('type', '')
    if t == 'phase':
        print(f"\n--- Phase {data['phase']} ({data['total']} epochs) ---")
    elif t == 'epoch':
        print(f"  Ep {data['epoch']:2d}/{data['total']}  "
              f"loss {data['tl']:.4f}/{data['vl']:.4f}  "
              f"acc {data['ta']}%/{data['va']}%  "
              f"lr {data['lr']:.2e}")
    elif t == 'log':
        print(f"  {data['msg']}")
    elif t == 'weights':
        w = data['weights']
        print(f"  weights: {w}")
    elif t == 'confusion':
        print(f"\n  Weighted F1: {data['weighted_f1']}  |  Cohen's k: {data['kappa']}")
        print(f"  Test set: {data['test_n']} ภาพ ({'separate' if data['is_test'] else 'val as test'})")
    elif t == 'class_metric':
        print(f"  {data['label']:15s} P={data['precision']:.3f} R={data['recall']:.3f} F1={data['f1']:.3f} (n={data['support']})")
    elif t == 'done':
        print(f"\n  {data['msg']}")
    elif t == 'error':
        print(f"  ERROR: {data['msg']}")

print("=== VitroVision Training Test ===")
stats = trainer.get_stats(DB_PATH, BASE_DIR)
print(f"Dataset: {stats['total']} images — {stats['per_class']}")
print(f"Starting training (head={cfg['epochs_head']} ep, fine-tune={cfg['epochs_full']} ep)...\n")

trainer.run_training(DB_PATH, BASE_DIR, MODEL_OUT, cfg, on_log)

if MODEL_OUT.exists():
    size_kb = MODEL_OUT.stat().st_size // 1024
    print(f"\nModel saved: {MODEL_OUT} ({size_kb} KB)")
