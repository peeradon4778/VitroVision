import sys
sys.path.insert(0, '.')
from pathlib import Path
import trainer, base64

previews = trainer.get_preview(Path('vitroshelf.db'), Path('.'), n=8)
print(f'Preview count: {len(previews)}')
for p in previews:
    print(f"  {p['label']:15s}  orig={len(p['original'])}B  aug={len(p['augmented'])}B")

# บันทึก 1 คู่ตัวอย่างเพื่อดูภาพ
if previews:
    sample = previews[0]
    with open('preview_orig.jpg', 'wb') as f:
        f.write(base64.b64decode(sample['original']))
    with open('preview_aug.jpg', 'wb') as f:
        f.write(base64.b64decode(sample['augmented']))
    print(f"Saved preview_orig.jpg + preview_aug.jpg (label={sample['label']})")
