from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import io
import json
import os
import threading
import queue
from PIL import Image

TOKEN_FILE = "oauth_token.json"
ROOT_FOLDER_ID = "1Utzy-D9X4Tzd7_VU0B7v_whk0WCnRQMs"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

_service = None
_folder_cache = {}


def _get_service():
    global _service
    if _service is not None:
        return _service
    with open(TOKEN_FILE) as f:
        data = json.load(f)
    creds = Credentials(
        token=data["token"],
        refresh_token=data["refresh_token"],
        token_uri=data["token_uri"],
        client_id=data["client_id"],
        client_secret=data["client_secret"],
        scopes=data["scopes"],
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        data["token"] = creds.token
        with open(TOKEN_FILE, "w") as f:
            json.dump(data, f, indent=2)
    _service = build("drive", "v3", credentials=creds, cache_discovery=False)
    return _service


def _get_or_create_folder(name, parent_id):
    cache_key = (name, parent_id)
    if cache_key in _folder_cache:
        return _folder_cache[cache_key]

    svc = _get_service()
    q = f"name='{name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = svc.files().list(q=q, fields="files(id)").execute()
    files = results.get("files", [])
    if files:
        folder_id = files[0]["id"]
    else:
        meta = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id],
        }
        folder = svc.files().create(body=meta, fields="id").execute()
        folder_id = folder["id"]

    _folder_cache[cache_key] = folder_id
    return folder_id


def _compress(image_bytes, max_size=640, quality=72):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode != "RGB":
            img = img.convert("RGB")
        w, h = img.size
        side = min(w, h)
        img = img.crop(((w - side) // 2, (h - side) // 2,
                        (w + side) // 2, (h + side) // 2))
        if side > max_size:
            img = img.resize((max_size, max_size), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        return buf.getvalue()
    except Exception:
        return image_bytes


def _save_local(bottle_id, day_point, image_id, status, image_bytes):
    shelf = bottle_id.split("-")[0]
    folder = os.path.join(DATA_DIR, shelf, bottle_id)
    os.makedirs(folder, exist_ok=True)
    filename = f"{bottle_id}_day{day_point:03d}_{image_id:04d}_{status}.jpg"
    path = os.path.join(folder, filename)
    with open(path, "wb") as f:
        f.write(image_bytes)
    return path


def upload_image(bottle_id, day_point, image_id, status, image_bytes, mimetype="image/jpeg"):
    image_bytes = _compress(image_bytes)
    local_path = _save_local(bottle_id, day_point, image_id, status, image_bytes)

    svc = _get_service()
    shelf = bottle_id.split("-")[0]
    shelf_folder = _get_or_create_folder(shelf, ROOT_FOLDER_ID)
    bottle_folder = _get_or_create_folder(bottle_id, shelf_folder)
    filename = f"{bottle_id}_day{day_point:03d}_{image_id:04d}_{status}.jpg"
    meta = {"name": filename, "parents": [bottle_folder]}
    media = MediaIoBaseUpload(io.BytesIO(image_bytes), mimetype=mimetype)
    file = svc.files().create(body=meta, media_body=media, fields="id, webViewLink").execute()
    return file["id"], file["webViewLink"], local_path


_upload_queue = queue.Queue()
_worker_thread = None


def _worker():
    import database as db
    while True:
        task = _upload_queue.get()
        if task is None:
            break
        image_id, bottle_id, day_point, status, image_bytes = task
        try:
            file_id, url, _ = upload_image(bottle_id, day_point, image_id, status, image_bytes)
            db.update_image_drive(image_id, file_id, url)
        except Exception as e:
            print(f"[Drive] background upload error img={image_id}: {e}")
        finally:
            _upload_queue.task_done()


def queue_upload(image_id, bottle_id, day_point, status, image_bytes):
    """บันทึก local ทันที แล้ว queue Drive upload ใน background"""
    global _worker_thread
    import database as db
    compressed = _compress(image_bytes)
    local_path = _save_local(bottle_id, day_point, image_id, status, compressed)
    db.update_image_local_path(image_id, local_path)
    if _worker_thread is None or not _worker_thread.is_alive():
        _worker_thread = threading.Thread(target=_worker, daemon=True)
        _worker_thread.start()
    _upload_queue.put((image_id, bottle_id, day_point, status, compressed))


def get_image_url(file_id):
    svc = _get_service()
    try:
        file = svc.files().get(fileId=file_id, fields="webViewLink").execute()
        return file.get("webViewLink")
    except Exception:
        return None
