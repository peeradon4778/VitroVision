"""
supabase_sync.py
Sync layer ระหว่าง SQLite (local) ↔ Supabase (cloud)

ฟังก์ชันหลัก:
  push_image(row_dict)  — push image record ไปยัง Supabase หลัง save local
  pull_mobile()         — ดึง captures จาก mobile ที่ยังไม่ sync มาเก็บ local
  mark_synced(ids)      — mark rows ว่า sync แล้ว
  status()              — เช็คว่า Supabase เชื่อมต่อได้ไหม
"""
from __future__ import annotations
import os, threading
from pathlib import Path

_URL = ''
_KEY = ''
_client = None
_lock   = threading.Lock()

def _load_env():
    global _URL, _KEY
    env = Path(__file__).parent.parent / '.env'
    if env.exists():
        for line in env.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            k = k.strip(); v = v.strip()
            if k == 'SUPABASE_URL': _URL = v
            if k == 'SUPABASE_KEY': _KEY = v
    _URL = _URL or os.environ.get('SUPABASE_URL', '')
    _KEY = _KEY or os.environ.get('SUPABASE_KEY', '')

_load_env()

def _sb():
    global _client
    if _client:
        return _client
    if not _URL or not _KEY:
        return None
    with _lock:
        if _client:
            return _client
        try:
            from supabase import create_client
            _client = create_client(_URL, _KEY)
        except Exception as e:
            print(f'[Supabase] init error: {e}')
    return _client


def push_image(row: dict):
    """Push image dict to Supabase. Fails silently (don't break local workflow)."""
    sb = _sb()
    if not sb:
        return
    try:
        data = {k: v for k, v in row.items() if k != 'local_path'}
        data.setdefault('source', 'desktop')
        data.setdefault('synced_local', True)
        sb.table('images').upsert(data, on_conflict='id').execute()
    except Exception as e:
        print(f'[Supabase] push_image failed: {e}')


def push_image_async(row: dict):
    """Push ใน background thread เพื่อไม่บล็อก response"""
    t = threading.Thread(target=push_image, args=(row,), daemon=True)
    t.start()


def pull_mobile(batch_id: int | None = None) -> list[dict]:
    """
    ดึง images ที่ถ่ายจากมือถือ (source='mobile', synced_local=false)
    คืน list ของ dict พร้อม insert เข้า SQLite
    """
    sb = _sb()
    if not sb:
        return []
    try:
        q = (sb.table('images')
               .select('*')
               .eq('source', 'mobile')
               .eq('synced_local', False))
        if batch_id:
            q = q.eq('batch_id', batch_id)
        return q.execute().data or []
    except Exception as e:
        print(f'[Supabase] pull_mobile failed: {e}')
        return []


def mark_synced(image_ids: list[int]):
    """Mark rows ใน Supabase ว่าถูก sync ลง local แล้ว"""
    sb = _sb()
    if not sb or not image_ids:
        return
    try:
        sb.table('images').update({'synced_local': True}).in_('id', image_ids).execute()
    except Exception as e:
        print(f'[Supabase] mark_synced failed: {e}')


def push_batch(batch_row: dict):
    """Push batch record ไปยัง Supabase"""
    sb = _sb()
    if not sb:
        return
    try:
        sb.table('batches').upsert(batch_row, on_conflict='id').execute()
    except Exception as e:
        print(f'[Supabase] push_batch failed: {e}')


def push_phenotype_series(record: dict):
    """Push phenotype_series record ไปยัง Supabase — fails silently"""
    sb = _sb()
    if not sb:
        return
    try:
        sb.table('phenotype_series').upsert(record, on_conflict='id').execute()
    except Exception as e:
        print(f'[Supabase] push_phenotype_series failed: {e}')


def push_phenotype_series_async(record: dict):
    """Push ใน background thread"""
    t = threading.Thread(target=push_phenotype_series, args=(record,), daemon=True)
    t.start()


def status() -> dict:
    """เช็ค connectivity พร้อม URL"""
    if not _URL or not _KEY:
        return {'ok': False, 'reason': 'ยังไม่ตั้งค่า SUPABASE_URL/KEY ใน .env'}
    sb = _sb()
    if not sb:
        return {'ok': False, 'reason': 'supabase package ไม่ได้ติดตั้ง'}
    try:
        sb.table('batches').select('id').limit(1).execute()
        return {'ok': True, 'url': _URL}
    except Exception as e:
        return {'ok': False, 'reason': str(e)}
