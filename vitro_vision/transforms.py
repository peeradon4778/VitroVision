"""Preprocessing + augmentation pipeline กลาง — ใช้ร่วมกันระหว่าง trainer.py และ VitroShelf"""
import albumentations as A
from albumentations.pytorch import ToTensorV2

_MEAN = [0.485, 0.456, 0.406]
_STD  = [0.229, 0.224, 0.225]


def get_train_transforms(size: int = 224) -> A.Compose:
    return A.Compose([
        A.RandomResizedCrop(height=size, width=size, scale=(0.65, 1.0)),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.3),
        A.RandomRotate90(p=0.5),
        A.ColorJitter(brightness=0.35, contrast=0.35, saturation=0.3, hue=0.0, p=0.8),
        A.GaussianBlur(blur_limit=(3, 7), p=0.3),
        A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
        A.Normalize(mean=_MEAN, std=_STD),
        ToTensorV2(),
    ])


def get_val_transforms(size: int = 224) -> A.Compose:
    return A.Compose([
        A.Resize(size, size),
        A.Normalize(mean=_MEAN, std=_STD),
        ToTensorV2(),
    ])
