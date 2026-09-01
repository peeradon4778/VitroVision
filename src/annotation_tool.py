"""Annotation tool — ป้าย/แก้ mask มือ (ground truth) ของต้นในขวดผ่านเบราว์เซอร์

สำหรับงานเลเวล A (mIoU/Dice เทียบมนุษย์) — ใช้ร่วมกับ `VALIDATION_PLAN.md` §2.2
ตัวช่วย: โหลด seed mask จาก SAM3 (pseudo) มาให้แก้ ไม่ต้องวาดใหม่ทั้งภาพ

รัน:
    python src/annotation_tool.py --data data/raw/20260814_batch \
        [--seed /path/to/pseudo_masks] --out data/processed/ground_truth_masks \
        --port 5000 --canvas-size 1024

เปิดเบราว์เซอร์ที่ http://localhost:5000
- ป้ายขาว/เขียว = ต้น (mask) · ปุ่ม Erase = ลบ
- บันทึกแล้วอัปเดตอัตโนมัติเป็น PNG ใน --out (ชื่อตามภาพ, threshold alpha>40)
- seed (ถ้ามี) วาดเป็นสีเขียว, ส่วนที่คุณเพิ่มเป็นสีขาว (export รวมทั้งคู่)
"""

import argparse
import base64
import glob
import io
import os
import sys

import cv2
import numpy as np
from flask import Flask, jsonify, render_template_string, request, send_from_directory

app = Flask(__name__)
ctx = {}

# ---------------------------------------------------------------- helpers
def binary_from_b64(b64img):
    """ถอด base64 PNG data-url → binary mask (uint8 0/255) ตาม alpha>40"""
    if b64img.startswith("data:"):
        b64img = b64img.split(",", 1)[1]
    raw = base64.b64decode(b64img)
    arr = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_UNCHANGED)
    if arr is None:
        return None
    if arr.ndim == 3:
        alpha = arr[..., 3] if arr.shape[2] == 4 else arr[..., 0]
    else:
        alpha = arr
    mask = (alpha > 40).astype(np.uint8) * 255
    return mask


# ---------------------------------------------------------------- routes
@app.route("/")
def index():
    return render_template_string(HTML, images=ctx["images"],
                                  has_seed=ctx["has_seed"],
                                  total=len(ctx["images"]))


@app.route("/img/<path:name>")
def img(name):
    return send_from_directory(ctx["data"], name)


@app.route("/seed/<path:name>")
def seed(name):
    stem = os.path.splitext(name)[0] + ".png"
    p = os.path.join(ctx["seed"], stem)
    if os.path.exists(p):
        return send_from_directory(ctx["seed"], stem)
    return ("", 404)


@app.route("/save/<path:name>", methods=["POST"])
def save(name):
    data = request.get_json() or {}
    b64 = data.get("image")
    mask = binary_from_b64(b64) if b64 else None
    if mask is None:
        return jsonify({"ok": False, "error": "no image"}), 400
    stem = os.path.splitext(name)[0]
    os.makedirs(ctx["out"], exist_ok=True)
    out_path = os.path.join(ctx["out"], stem + ".png")
    cv2.imwrite(out_path, mask)
    done = len(glob.glob(os.path.join(ctx["out"], "*.png")))
    return jsonify({"ok": True, "saved": stem, "done": done, "total": ctx["total"]})


@app.route("/stats")
def stats():
    done = len(glob.glob(os.path.join(ctx["out"], "*.png")))
    return jsonify({"done": done, "total": ctx["total"]})


# ---------------------------------------------------------------- index page
HTML = r"""<!doctype html><html lang="th"><head><meta charset="utf-8">
<title>VitroVision — annotate mask</title>
<style>
  body{font-family:sans-serif;margin:0;background:#111;color:#eee;display:flex;flex-direction:column;height:100vh}
  #bar{display:flex;gap:12px;align-items:center;padding:8px 14px;background:#1c1c1c;flex-wrap:wrap;font-size:14px}
  #bar b{color:#7CFC8A}
  .btn{background:#2a2a2a;border:1px solid #444;color:#eee;padding:6px 12px;border-radius:6px;cursor:pointer;font-size:14px}
  .btn.active{background:#1B5E20;border-color:#2E7D32}
  .btn:hover{background:#3a3a3a}
  #stage{flex:1;position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center;background:#000}
  canvas{position:absolute;touch-action:none}
  #nav{position:absolute;bottom:12px;left:0;right:0;display:flex;justify-content:center;gap:10px;z-index:5}
  #info{position:absolute;top:12px;left:14px;z-index:5;background:rgba(0,0,0,.6);padding:6px 10px;border-radius:6px;font-size:13px}
  input[type=range]{width:140px}
  #side{background:#1c1c1c;padding:10px;display:flex;flex-direction:column;gap:8px;font-size:13px;min-width:160px}
  #wrap{display:flex;height:100%}
  #list{max-height:100%;overflow:auto;font-size:12px}
  #list .item{padding:3px 6px;cursor:pointer}
  #list .item.done{color:#7CFC8A}
  #list .item.cur{background:#2E7D32}
</style></head><body>
<div id="bar">
  <b>VitroVision annotate</b>
  <span id="prog">0/0</span>
  <span id="seednote"></span>
  <button class="btn" id="btnAdd">✏️ เพิ่ม (mask)</button>
  <button class="btn" id="btnErase">🧽 ลบ</button>
  <label>ขนาด: <input type="range" id="brush" min="4" max="120" value="30"></label>
  <button class="btn" id="btnUndo">↩ Undo</button>
  <button class="btn" id="btnClear">🗑 Clear</button>
  <button class="btn" id="btnSave" style="background:#1B5E20">💾 บันทึก & ถัดไป</button>
</div>
<div id="wrap">
  <div id="stage">
    <canvas id="cv"></canvas>
    <div id="info"></div>
    <div id="nav">
      <button class="btn" id="prev">‹</button>
      <button class="btn" id="next">›</button>
    </div>
  </div>
  <div id="side"><div>รายการภาพ</div><div id="list"></div></div>
</div>
<script>
const IMAGES = {{ images | tojson }};
const HAS_SEED = {{ has_seed | tojson }};
const ctx = document.getElementById('cv').getContext('2d');
const cv = document.getElementById('cv');
let idx = 0, painting = false, mode = 'add', doneSet = new Set();
let img = new Image(); let seedImg = HAS_SEED ? new Image() : null;
let W = 1024, H = 1024;

function resizeCanvas(){
  // work at working-res (fit side / keep ~1400px) — export at this res
  const maxSide = 1400;
  const iw = img.naturalWidth || 1, ih = img.naturalHeight || 1;
  const s = Math.min(maxSide / iw, maxSide / ih, 1);
  W = Math.round(iw * s); H = Math.round(ih * s);
  cv.width = W; cv.height = H;
  stroke.width = W; stroke.height = H;
  cv.style.maxWidth = '92vw'; cv.style.maxHeight = '90vh';
  ctx.drawImage(img, 0, 0, W, H);
  if (seedImg && seedImg.complete && seedImg.naturalWidth){ applySeed(); }
}
function applySeed(){
  ctx.save(); ctx.globalAlpha=0.45; ctx.fillStyle='#00ff88';
  ctx.globalCompositeOperation='source-over';
  // tint seed region green
  const o=document.createElement('canvas'); o.width=W; o.height=H;
  const oo=o.getContext('2d'); oo.drawImage(seedImg,0,0,W,H);
  const d=oo.getImageData(0,0,W,H); const p=d.data;
  for(let i=0;i<p.length;i+=4){ if(p[i+3]>40){ p[i]=0;p[i+1]=230;p[i+2]=120;p[i+3]=220; } }
  oo.putImageData(d,0,0);
  ctx.drawImage(o,0,0);
  ctx.restore();
}
// We treat "mask layer" = stack of green seed + white strokes. For export we
// convert back to binary via alpha>40 in a fresh canvas.
function currentMask(){
  const o=document.createElement('canvas'); o.width=W; o.height=H;
  const oo=o.getContext('2d');
  if (seedImg && seedImg.complete && seedImg.naturalWidth){
    oo.drawImage(seedImg,0,0,W,H); // seed (its alpha encodes mask)
  }
  // stroked layer within ctx is already on cv; we rebuild by re-reading cv is hard.
  // Simpler: keep strokes on a dedicated transparent layer.
  return null;
}

// --- robust approach: dedicated transparent stroke-layer ---
const stroke = document.createElement('canvas');
let sctx = stroke.getContext('2d');
function strokeSize(){ stroke.width=W; stroke.height=H; redraw(); }
function redraw(){
  ctx.drawImage(img,0,0,W,H);          // photo
  if (seedImg && seedImg.complete && seedImg.naturalWidth) drawSeedOverlay();
  ctx.drawImage(stroke,0,0);           // user strokes (white)
}
let seedData = null;
function drawSeedOverlay(){
  if(!seedData){ // build green seed layer
    const o=document.createElement('canvas'); o.width=W; o.height=H;
    const oo=o.getContext('2d'); oo.drawImage(seedImg,0,0,W,H);
    const d=oo.getImageData(0,0,W,H), p=d.data;
    for(let i=0;i<p.length;i+=4){ const a=p[i+3];
      p[i]=60;p[i+1]=230;p[i+2]=120; p[i+3]=(a>40?200:a); }
    oo.putImageData(d,0,0);
    // convert to transparent, only where seed
    const o2=document.createElement('canvas'); o2.width=W; o2.height=H;
    o2.getContext('2d').clearRect(0,0,W,H);
    o2.getContext('2d').drawImage(o,0,0);
    seedData=o2;
  }
  ctx.globalAlpha=0.5; ctx.drawImage(seedData,0,0); ctx.globalAlpha=1;
}

function load(i){
  idx = (i+IMAGES.length)%IMAGES.length;
  clearUndo();
  sctx.clearRect(0,0,W,H);
  img.onload = ()=>{ resizeCanvas(); initStroke(); };
  img.src = '/img/' + encodeURIComponent(IMAGES[idx]);
  updateInfo();
}
function initStroke(){
  // reset stroke layer after canvas size known
  sctx.clearRect(0,0,W,H);
  sctx.lineWidth=30; sctx.lineCap='round'; sctx.lineJoin='round'; sctx.strokeStyle='#fff';
  redraw();
}
if(HAS_SEED){ seedImg.onload = ()=>{ seedData=null; }; }

// --- painting ---
function pos(e){ const r=cv.getBoundingClientRect(); return [ (e.clientX-r.left)*(cv.width/r.width), (e.clientY-r.top)*(cv.height/r.height) ]; }
cv.addEventListener('mousedown', e=>{ painting=true; const b=sctx; b.lineWidth=+document.getElementById('brush').value;
  b.strokeStyle='#fff'; b.globalAlpha=0.9; b.beginPath(); const [x,y]=pos(e); b.moveTo(x,y);
  if(mode!=='add') b.globalCompositeOperation='destination-out';
  else b.globalCompositeOperation='source-over';
  snapUndo(); });
cv.addEventListener('mousemove', e=>{ if(!painting)return; const [x,y]=pos(e); const b=sctx;
  const was=b.globalCompositeOperation; b.globalCompositeOperation=(mode!=='add')?'destination-out':'source-over';
  b.lineTo(x,y); b.stroke(); b.beginPath(); b.moveTo(x,y); });
cv.addEventListener('mouseup', ()=>{ painting=false; redraw(); });
// touch
cv.addEventListener('touchstart', e=>{ e.preventDefault(); painting=true; const t=e.touches[0];
  const b=sctx; b.lineWidth=+document.getElementById('brush').value; b.strokeStyle='#fff'; b.globalAlpha=0.9;
  b.globalCompositeOperation=(mode!=='add')?'destination-out':'source-over'; b.beginPath();
  const [x,y]=pos(t); b.moveTo(x,y); snapUndo(); },{passive:false});
cv.addEventListener('touchmove', e=>{ e.preventDefault(); if(!painting)return; const t=e.touches[0];
  const [x,y]=pos(t); const b=sctx; b.lineTo(x,y); b.stroke(); b.beginPath(); b.moveTo(x,y); },{passive:false});
cv.addEventListener('touchend', e=>{ e.preventDefault(); painting=false; redraw(); },{passive:false});

// --- undo / clear ---
const undoStack=[];
function snapUndo(){ if(undoStack.length>30)undoStack.shift();
  const o=document.createElement('canvas'); o.width=W;o.height=H; o.getContext('2d').drawImage(stroke,0,0); undoStack.push(o); }
function clearUndo(){ undoStack.length=0; }
function undo(){ const o=undoStack.pop(); if(!o)return; sctx.clearRect(0,0,W,H); sctx.drawImage(o,0,0); redraw(); }
function clearMask(){ sctx.clearRect(0,0,W,H); redraw(); }

// --- export mask (binary) ---
function exportMask(){
  const o=document.createElement('canvas'); o.width=W;o.height=H; const oo=o.getContext('2d');
  oo.clearRect(0,0,W,H);
  if (seedData){ oo.globalAlpha=1; oo.drawImage(seedData,0,0); }   // seed
  // threshold user strokes by alpha
  const so=document.createElement('canvas'); so.width=W;so.height=H; const sc=so.getContext('2d');
  sc.drawImage(stroke,0,0);
  const d=sc.getImageData(0,0,W,H), p=d.data;
  for(let i=0;i<p.length;i+=4){ p[i]=p[i+1]=p[i+2]= (p[i+3]>40?255:0); p[i+3]=255; }
  sc.putImageData(d,0,0);
  // combine: OR seed+strokes into oo (white), then we save binary
  oo.globalCompositeOperation='source-over';
  // convert seed to white binary too
  const sd=seedData?seedData.getContext('2d').getImageData(0,0,W,H):null;
  if(sd){ const sp=sd.data; for(let i=0;i<sp.length;i+=4){ sp[i]=sp[i+1]=sp[i+2]=(sp[i+3]>40?255:0); sp[i+3]=255; } seedData.getContext('2d').putImageData(sd,0,0);}
  oo.drawImage(seedData||stroke,0,0);
  oo.globalCompositeOperation='source-over';
  oo.drawImage(so,0,0);
  return o.toDataURL('image/png');
}

async function save(goNext){
  const data={image:exportMask()};
  const res=await fetch('/save/'+encodeURIComponent(IMAGES[idx]),{method:'POST',
    headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)});
  const j=await res.json();
  document.getElementById('prog').textContent=`${j.done}/${j.total}`;
  doneSet.add(IMAGES[idx]); markList();
  if(goNext && !(idx===IMAGES.length-1)) load(idx+1);
  // if last, show done message
  if(j.done>=j.total && !goNext) alert('ครบแล้ว! 🎉');
}

function updateInfo(){ document.getElementById('info').textContent = `${idx+1}/${IMAGES.length} · ${IMAGES[idx]}`;
  markList(); if(seedImg&&HAS_SEED) document.getElementById('seednote').textContent='seed ✓ (เขียว=แก้ได้)'; }
function markList(){ document.querySelectorAll('#list .item').forEach((el,k)=>{ el.classList.toggle('done',doneSet.has(IMAGES[k])); el.classList.toggle('cur',k===idx); }); }

// --- controls ---
document.getElementById('btnAdd').onclick=()=>{mode='add';document.getElementById('btnAdd').classList.add('active');document.getElementById('btnErase').classList.remove('active');};
document.getElementById('btnErase').onclick=()=>{mode='erase';document.getElementById('btnErase').classList.add('active');document.getElementById('btnAdd').classList.remove('active');};
document.getElementById('btnUndo').onclick=undo;
document.getElementById('btnClear').onclick=clearMask;
document.getElementById('btnSave').onclick=()=>save(true);
document.getElementById('prev').onclick=()=>load(idx-1);
document.getElementById('next').onclick=()=>load(idx+1);
window.addEventListener('keydown',e=>{ if(e.key==='ArrowRight')load(idx+1); if(e.key==='ArrowLeft')load(idx-1); if(e.key==='s')save(true); });

async function init(){
  document.getElementById('btnAdd').classList.add('active');
  const s=await (await fetch('/stats')).json();
  document.getElementById('prog').textContent=`${s.done}/${s.total}`;
  document.getElementById('prog').dataset.total=s.total;
  // list
  const list=document.getElementById('list');
  IMAGES.forEach((n,k)=>{ const el=document.createElement('div'); el.className='item'; el.textContent=n;
    el.onclick=()=>load(k); list.appendChild(el); });
  load(0);
}
init();
</script></body></html>
"""


# ---------------------------------------------------------------- main
def main():
    # กัน print ภาษาไทย crash บน console Windows (cp1252)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Annotation tool (ground-truth masks)")
    ap.add_argument("--data", required=True, help="โฟลเดอร์ภาพ")
    ap.add_argument("--seed", default=None, help="โฟลเดอร์ seed masks จาก SAM3 (optional)")
    ap.add_argument("--out", default="data/processed/ground_truth_masks", help="โฟลเดอร์ผล mask")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=5000)
    ap.add_argument("--debug", action="store_true")
    args = ap.parse_args()

    ext = ("*.jpg", "*.jpeg", "*.png", "*.JPG")
    images = sorted({f for e in ext for f in glob.glob(os.path.join(args.data, e))})
    images = [os.path.basename(p) for p in images]
    if not images:
        raise SystemExit(f"ไม่พบภาพใน {args.data}")

    ctx["data"] = os.path.abspath(args.data)
    ctx["seed"] = os.path.abspath(args.seed) if args.seed else ""
    ctx["out"] = os.path.abspath(args.out)
    ctx["images"] = images
    ctx["total"] = len(images)
    ctx["has_seed"] = bool(args.seed and os.path.isdir(args.seed))

    print(f"[INFO] ภาพ {len(images)} · seed={'มี' if ctx['has_seed'] else 'ไม่มี'} "
          f"· out={ctx['out']}")
    print(f"[INFO] เปิด http://{args.host}:{args.port} ในเบราว์เซอร์")
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
