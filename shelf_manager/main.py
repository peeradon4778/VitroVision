import json, time, threading
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import database as db
import drive_uploader as drive
import socket

# ── ML modules — โหลดใน background thread (ไม่บล็อก startup) ──
_trainer    = None
_inference  = None
_phenotyper = None
_aruco      = None
TRAINER_OK  = False
INFERENCE_OK= False
PHENOTYPER_OK=False
ARUCO_OK    = False
_ml_ready   = False

def _load_ml():
    global _trainer, _inference, _phenotyper, _aruco
    global TRAINER_OK, INFERENCE_OK, PHENOTYPER_OK, ARUCO_OK, _ml_ready
    try:
        import trainer as m; _trainer = m; TRAINER_OK = True
    except Exception: pass
    try:
        import inference as m; _inference = m; INFERENCE_OK = True
    except Exception: pass
    try:
        import phenotyper as m; _phenotyper = m; PHENOTYPER_OK = True
    except Exception: pass
    try:
        import aruco_map as m; _aruco = m; ARUCO_OK = m.ARUCO_OK
    except Exception:
        class _stub:
            @staticmethod
            def detect(b): return []
            @staticmethod
            def calc_clarity(c): return 0
        _aruco = _stub()
    _ml_ready = True

threading.Thread(target=_load_ml, daemon=True).start()

# ── Active Learning config ────────────────────────────────────
_AL_CONFIG = Path(__file__).parent / 'al_config.json'
_AL_DEFAULT = {'threshold': 20, 'count_since_retrain': 0, 'last_retrain_at': ''}

def _al_load():
    if _AL_CONFIG.exists():
        try:
            with open(_AL_CONFIG) as f:
                cfg = json.load(f)
                return {**_AL_DEFAULT, **cfg}
        except Exception:
            pass
    return dict(_AL_DEFAULT)

def _al_save(cfg):
    with open(_AL_CONFIG, 'w') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def _al_increment_and_check(status):
    """เพิ่ม counter และ trigger auto-retrain ถ้าถึง threshold"""
    if status not in ('healthy', 'contaminated', 'dead'):
        return
    cfg = _al_load()
    cfg['count_since_retrain'] = cfg.get('count_since_retrain', 0) + 1
    _al_save(cfg)
    if cfg['count_since_retrain'] >= cfg.get('threshold', 20):
        _auto_retrain(cfg)

def _auto_retrain(cfg):
    global _is_training, _log_buf
    if _is_training or not TRAINER_OK:
        return
    cfg['count_since_retrain'] = 0
    cfg['last_retrain_at'] = time.strftime('%Y-%m-%d %H:%M')
    _al_save(cfg)
    with _buf_lock:
        _log_buf = []
    _is_training = True
    def _run():
        global _is_training
        _on_log({'type': 'log', 'msg': '🤖 Auto-retrain เริ่มต้น (Active Learning)'})
        _trainer.run_training(_DB_PATH, _BASE_DIR, _MODEL_OUT,
                              {'epochs_head': 10, 'epochs_full': 20, 'lr': 1e-4}, _on_log)
        _is_training = False
    threading.Thread(target=_run, daemon=True).start()

# ── Glass Room event log ──────────────────────────────────────
import collections
_glass_log   = collections.deque(maxlen=300)
_glass_lock  = threading.Lock()
_glass_state = {}   # bottle_id → {state, clarity, time, status}

def _glass_event(ev: dict):
    with _glass_lock:
        _glass_log.append(ev)
        bid = ev.get('bottle_id')
        if bid:
            _glass_state[bid] = {
                'state':   ev['type'],
                'clarity': ev.get('clarity', 0),
                'time':    ev.get('time', ''),
                'status':  ev.get('status', 'unknown'),
            }

_MODEL_OUT   = Path(__file__).parent.parent / 'models' / 'final' / 'classifier.pt'
_DB_PATH     = Path(__file__).parent / 'vitroshelf.db'
_BASE_DIR    = Path(__file__).parent
_log_buf     = []
_is_training = False
_buf_lock    = threading.Lock()


def _on_log(data):
    with _buf_lock:
        _log_buf.append(data)

app = Flask(__name__)


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"


@app.route("/api/ml_status")
def ml_status():
    return jsonify({
        'ready':     _ml_ready,
        'trainer':   TRAINER_OK,
        'inference': INFERENCE_OK,
        'phenotyper':PHENOTYPER_OK,
        'aruco':     ARUCO_OK,
    })

@app.route("/")
def index():
    stats = db.get_stats()
    local_ip = get_local_ip()
    grids = {shelf: db.get_shelf_grid(shelf) for shelf in db.SHELVES}
    batches = db.get_all_batches()
    return render_template("index.html", shelves=db.SHELVES, stats=stats,
                           local_ip=local_ip, port=5001,
                           grids=grids, rows=db.ROWS, cols=db.COLS,
                           batches=batches)


@app.route("/batch/new", methods=["POST"])
def new_batch():
    name       = request.form.get("name", "").strip()
    round_type = request.form.get("round_type", "training")
    start_date = request.form.get("start_date", "")
    notes      = request.form.get("notes", "")
    if not name or not start_date:
        return redirect(url_for("index"))
    batch_id = db.create_batch(name, round_type, start_date, notes)
    db.start_new_round(batch_id)
    return redirect(url_for("index"))


@app.route("/shelf/<shelf_id>")
def shelf_view(shelf_id):
    if shelf_id not in db.SHELVES:
        return redirect(url_for("index"))
    grid = db.get_shelf_grid(shelf_id)
    return render_template("shelf.html", shelf_id=shelf_id, grid=grid,
                           rows=db.ROWS, cols=db.COLS)


@app.route("/bottle/<bottle_id>")
def bottle_detail(bottle_id):
    bottle, images = db.get_bottle(bottle_id)
    if not bottle:
        return redirect(url_for("index"))
    next_id = db.get_next_bottle_id(bottle_id)
    return render_template("bottle.html", bottle=bottle, images=images,
                           status_choices=db.STATUS_CHOICES, next_bottle_id=next_id)


@app.route("/bottle/<bottle_id>/update", methods=["POST"])
def update_bottle(bottle_id):
    db.update_bottle_info(
        bottle_id,
        request.form.get("species", ""),
        request.form.get("treatment", ""),
        request.form.get("date_planted", ""),
        request.form.get("notes", ""),
        cultivar=request.form.get("cultivar", ""),
        media_formula=request.form.get("media_formula", ""),
        pgr_detail=request.form.get("pgr_detail", ""),
        passage_number=int(request.form.get("passage_number", 1) or 1),
    )
    return redirect(url_for("bottle_detail", bottle_id=bottle_id))


@app.route("/bottle/<bottle_id>/add_record", methods=["POST"])
def add_record(bottle_id):
    day_point = int(request.form.get("day_point", 0))
    status = request.form.get("status", "unknown")
    image_id = db.add_image(bottle_id, day_point, status)
    if "photo" in request.files and request.files["photo"].filename:
        image_bytes = request.files["photo"].read()
        try:
            file_id, url, local_path = drive.upload_image(bottle_id, day_point, image_id, status, image_bytes)
            db.update_image_drive(image_id, file_id, url)
            db.update_image_local_path(image_id, local_path)
        except Exception as e:
            print(f"Drive upload error: {e}")
    return redirect(url_for("bottle_detail", bottle_id=bottle_id))


@app.route("/api/phenotype", methods=["POST"])
def api_phenotype():
    if not PHENOTYPER_OK:
        return jsonify({'error': 'phenotyper ไม่พร้อม'}), 503
    if 'photo' not in request.files or not request.files['photo'].filename:
        return jsonify({'error': 'ไม่มีภาพ'}), 400
    image_bytes = request.files['photo'].read()
    result = _phenotyper.measure(image_bytes)
    result['seg_model_ready'] = _phenotyper.seg_model_ready()
    return jsonify(result)


@app.route("/api/phenotype/series/<bottle_id>")
def api_phenotype_series(bottle_id):
    return jsonify(db.get_phenotype_series(bottle_id))


@app.route("/api/bottle_timeline/<bottle_id>")
def api_bottle_timeline(bottle_id):
    return jsonify(db.get_bottle_timeline(bottle_id))


@app.route("/api/predict", methods=["POST"])
def api_predict():
    if not INFERENCE_OK or not _inference.ready():
        return jsonify({'ai_status': 'unknown', 'ai_confidence': 0.0, 'model_ready': False})
    if 'photo' not in request.files or not request.files['photo'].filename:
        return jsonify({'error': 'ไม่มีภาพ'}), 400
    image_bytes = request.files['photo'].read()
    label, conf = _inference.predict_bytes(image_bytes)
    return jsonify({'ai_status': label, 'ai_confidence': conf, 'model_ready': True})


@app.route("/bottle/<bottle_id>/add_record_json", methods=["POST"])
def add_record_json(bottle_id):
    day_point    = int(request.form.get("day_point", 0))
    status       = request.form.get("status", "unknown")
    shoot_count  = int(request.form.get("shoot_count", -1) or -1)
    shoot_height = request.form.get("shoot_height_class", "")
    root_density = request.form.get("root_density", "none")
    callus       = int(request.form.get("callus_present", 0) or 0)
    vigor        = int(request.form.get("vigor_score", 0) or 0)
    image_bytes  = None
    if "photo" in request.files and request.files["photo"].filename:
        image_bytes = request.files["photo"].read()
    image_id = db.add_image(
        bottle_id, day_point, status,
        shoot_count=shoot_count, shoot_height_class=shoot_height,
        root_density=root_density, callus_present=callus, vigor_score=vigor,
    )
    ai_status, ai_conf = 'unknown', 0.0
    pheno = {}
    if image_bytes:
        drive.queue_upload(image_id, bottle_id, day_point, status, image_bytes)
        if INFERENCE_OK and _inference.ready():
            ai_status, ai_conf = _inference.predict_bytes(image_bytes)
            db.update_image_cv(image_id, shoot_count, 'normal', False, False,
                               ai_status, ai_conf)
        if PHENOTYPER_OK:
            pheno = _phenotyper.measure(image_bytes)
            if pheno:
                db.update_image_phenotype(
                    image_id,
                    pheno.get('green_coverage_pct'),
                    pheno.get('leaf_color_index'),
                    pheno.get('shoot_count_cv'),
                    pheno.get('media_color_cv', ''),
                    pheno.get('method', ''),
                    texture_entropy=pheno.get('texture_entropy'),
                    brown_coverage_pct=pheno.get('brown_coverage_pct'),
                    vigor_score=pheno.get('vigor_score'),
                )
    _al_increment_and_check(status)
    return jsonify({"ok": True, "ai_status": ai_status, "ai_confidence": ai_conf,
                    "phenotype": pheno})


@app.route("/image/<int:image_id>")
def get_image(image_id):
    url = db.get_image_url(image_id)
    if not url:
        return "", 404
    return jsonify({"url": url})


# --- VitroVision API ---

@app.route("/api/bottle/<bottle_id>")
def api_bottle(bottle_id):
    bottle, images = db.get_bottle(bottle_id)
    if not bottle:
        return jsonify({"error": "ไม่พบขวด"}), 404
    return jsonify({
        "bottle": bottle,
        "images": images,
    })


@app.route("/api/bottle/<bottle_id>/observation", methods=["POST"])
def api_add_observation(bottle_id):
    bottle, _ = db.get_bottle(bottle_id)
    if not bottle:
        return jsonify({"error": "ไม่พบขวด"}), 404

    data = request.get_json(force=True) or {}
    day_point    = int(data.get("day_point", 0))
    status       = data.get("status", "unknown")
    shoot_count  = int(data.get("shoot_count", -1))
    media_color  = data.get("media_color", "normal")
    hyperhydricity = bool(data.get("hyperhydricity", False))
    has_roots    = bool(data.get("has_roots", False))
    ai_status    = data.get("ai_status", "")
    ai_confidence = float(data.get("ai_confidence", 0.0))

    image_id = db.add_image(
        bottle_id, day_point, status,
        shoot_count=shoot_count, media_color=media_color,
        hyperhydricity=hyperhydricity, has_roots=has_roots,
    )
    db.update_image_cv(image_id, shoot_count, media_color,
                       hyperhydricity, has_roots, ai_status, ai_confidence)

    return jsonify({"ok": True, "image_id": image_id})


# --- Active Learning Status ---

@app.route('/train/al_status')
def train_al_status():
    cfg       = _al_load()
    threshold = cfg.get('threshold', 20)
    count     = cfg.get('count_since_retrain', 0)
    return jsonify({
        'threshold':          threshold,
        'count_since_retrain': count,
        'pct':                min(round(count / threshold * 100), 100),
        'last_retrain_at':    cfg.get('last_retrain_at', ''),
        'is_training':        _is_training,
        'model_ready':        INFERENCE_OK and _inference.ready() if INFERENCE_OK else False,
    })

@app.route('/train/al_threshold', methods=['POST'])
def set_al_threshold():
    data = request.get_json(silent=True) or {}
    cfg  = _al_load()
    cfg['threshold'] = max(5, int(data.get('threshold', 20)))
    _al_save(cfg)
    return jsonify({'ok': True, 'threshold': cfg['threshold']})


@app.route('/api/al_query')
def api_al_query():
    n = int(request.args.get('n', 10))
    bottles = db.get_unlabeled_bottles()
    results = []
    for b in bottles:
        lp = b.get('local_path', '')
        if not lp or not Path(lp).exists():
            continue
        img_bytes = Path(lp).read_bytes()
        if not INFERENCE_OK:
            continue
        mc = _inference.predict_mc_dropout(img_bytes)
        results.append({
            'bottle_id':  b['bottle_id'],
            'shelf':      b['shelf'],
            'row':        b['row'],
            'col':        b['col'],
            'image_id':   b['image_id'],
            'local_path': lp,
            **mc,
        })
    results.sort(key=lambda x: x['uncertainty'], reverse=True)
    return jsonify(results[:n])


# --- VitroVision Trainer ---

@app.route('/train')
def train_page():
    import json as _json, datetime as _dt
    stats        = _trainer.get_stats(_DB_PATH, _BASE_DIR) if TRAINER_OK else {'total': 0, 'per_class': {'healthy': 0, 'contaminated': 0, 'dead': 0}, 'ready': False}
    model_exists = _MODEL_OUT.exists()
    model_info   = {}
    if model_exists:
        metrics_path = _MODEL_OUT.parent / 'metrics.json'
        if metrics_path.exists():
            try:
                with open(metrics_path, encoding='utf-8') as f:
                    m = _json.load(f)
                model_info = {
                    'f1':    round(m.get('weighted_f1', 0), 3),
                    'kappa': round(m.get('cohen_kappa', 0), 3),
                    'n_train': m.get('n_train', 0),
                    'n_test':  m.get('n_test', 0),
                    'mtime':   _dt.datetime.fromtimestamp(
                        _MODEL_OUT.stat().st_mtime
                    ).strftime('%Y-%m-%d %H:%M'),
                }
            except Exception:
                pass
    return render_template('train.html', stats=stats, model_exists=model_exists,
                           trainer_ok=TRAINER_OK, model_info=model_info)


@app.route('/train/preview')
def train_preview():
    if not TRAINER_OK:
        return jsonify({'error': 'trainer ไม่พร้อม'}), 503
    return jsonify(_trainer.get_preview(_DB_PATH, _BASE_DIR, n=8))


@app.route('/train/stats')
def train_stats():
    if not TRAINER_OK:
        return jsonify({'error': 'trainer ไม่พร้อม — รัน start.bat ด้วย conda ml'}), 503
    return jsonify(_trainer.get_stats(_DB_PATH, _BASE_DIR))


@app.route('/train/start', methods=['POST'])
def train_start():
    global _is_training, _log_buf
    if not TRAINER_OK:
        return jsonify({'error': 'trainer ไม่พร้อม — รัน start.bat ด้วย conda ml'}), 503
    if _is_training:
        return jsonify({'error': 'กำลัง train อยู่แล้ว'}), 400
    cfg = request.get_json(silent=True) or {}
    with _buf_lock:
        _log_buf = []
    _is_training = True

    def _run():
        global _is_training
        _trainer.run_training(_DB_PATH, _BASE_DIR, _MODEL_OUT, cfg, _on_log)
        _is_training = False

    threading.Thread(target=_run, daemon=True).start()
    return jsonify({'status': 'started'})


@app.route('/train/stop', methods=['POST'])
def train_stop():
    if TRAINER_OK:
        _trainer.stop()
    return jsonify({'status': 'stopping'})


@app.route('/train/stream')
def train_stream():
    def generate():
        sent = 0
        while True:
            with _buf_lock:
                new = _log_buf[sent:]
                sent += len(new)
            for msg in new:
                yield f'data: {json.dumps(msg, ensure_ascii=False)}\n\n'
                if msg.get('type') in ('done', 'error'):
                    # ล้าง buffer หลังจบ — ป้องกัน replay ตอน reconnect
                    with _buf_lock:
                        _log_buf.clear()
                    return
            time.sleep(0.4)
    return Response(generate(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})


@app.route('/api/scan_save', methods=['POST'])
def api_scan_save():
    bottle_id     = request.form.get('bottle_id', '').strip()
    day_point     = int(request.form.get('day_point', 0) or 0)
    ai_status     = request.form.get('ai_status', 'unknown')
    ai_confidence = float(request.form.get('ai_confidence', 0) or 0)
    bottle, _     = db.get_bottle(bottle_id)
    if not bottle:
        return jsonify({'error': 'ไม่พบขวด'}), 404
    status   = ai_status if ai_status in ('healthy', 'contaminated', 'dead') else 'unknown'
    image_id    = db.add_image(bottle_id, day_point, status)
    image_bytes = None
    if 'photo' in request.files and request.files['photo'].filename:
        image_bytes = request.files['photo'].read()
        drive.queue_upload(image_id, bottle_id, day_point, status, image_bytes)
        if status != 'unknown':
            db.update_image_cv(image_id, -1, 'normal', False, False, ai_status, ai_confidence)
    pheno = {}
    bottle_count = int(request.form.get('bottle_count', 1) or 1)
    if image_bytes and PHENOTYPER_OK and bottle_count == 1:
        pheno = _phenotyper.measure(image_bytes)
        if pheno:
            db.update_image_phenotype(
                image_id,
                pheno.get('green_coverage_pct'),
                pheno.get('leaf_color_index'),
                pheno.get('shoot_count_cv'),
                pheno.get('media_color_cv', ''),
                pheno.get('method', ''),
                texture_entropy=pheno.get('texture_entropy'),
                brown_coverage_pct=pheno.get('brown_coverage_pct'),
                vigor_score=pheno.get('vigor_score'),
            )
    _al_increment_and_check(status)
    _glass_event({
        'type':      'save',
        'bottle_id': bottle_id,
        'clarity':   int(request.form.get('clarity', 0) or 0),
        'status':    status,
        'time':      time.strftime('%H:%M:%S'),
        'green_pct': pheno.get('green_coverage_pct'),
        'lci':       pheno.get('leaf_color_index'),
        'media':     pheno.get('media_color_cv', ''),
    })
    return jsonify({'ok': True, 'image_id': image_id, 'bottle_id': bottle_id, 'phenotype': pheno})


@app.route('/glass')
def glass_page():
    return render_template('glass.html',
                           shelves=db.SHELVES, rows=db.ROWS, cols=db.COLS)

@app.route('/api/glass_stream')
def glass_stream():
    def generate():
        with _glass_lock:
            snapshot = list(_glass_log)
        for ev in snapshot[-30:]:
            yield f'data: {json.dumps(ev, ensure_ascii=False)}\n\n'
        sent = len(snapshot)
        while True:
            with _glass_lock:
                current = list(_glass_log)
            for ev in current[sent:]:
                yield f'data: {json.dumps(ev, ensure_ascii=False)}\n\n'
            sent = len(current)
            time.sleep(0.35)
    return Response(generate(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})

@app.route('/api/glass_state')
def glass_state_api():
    with _glass_lock:
        return jsonify(dict(_glass_state))

@app.route('/scan')
def scan_page():
    return render_template('scan.html', aruco_ok=ARUCO_OK)


@app.route('/api/scan_aruco', methods=['POST'])
def api_scan_aruco():
    if 'photo' not in request.files or not request.files['photo'].filename:
        return jsonify({'detections': []})
    image_bytes = request.files['photo'].read()
    raw         = _aruco.detect(image_bytes)
    model_ready = INFERENCE_OK and _inference.ready() if INFERENCE_OK else False
    detections  = []
    for item in raw:
        bottle, _ = db.get_bottle(item['bottle_id'])
        ai_status, ai_conf = 'unknown', 0.0
        if model_ready:
            ai_status, ai_conf = _inference.predict_bytes(image_bytes)
        detections.append({
            'bottle_id':     item['bottle_id'],
            'corners':       item['corners'],
            'frame_w':       item['frame_w'],
            'frame_h':       item['frame_h'],
            'bottle':        bottle,
            'ai_status':     ai_status,
            'ai_confidence': ai_conf,
        })
    for item in detections:
        clarity = _aruco.calc_clarity(item['corners']) if ARUCO_OK else 0
        _glass_event({
            'type':      'detect',
            'bottle_id': item['bottle_id'],
            'clarity':   clarity,
            'status':    (item['bottle'] or {}).get('status', 'unknown'),
            'time':      time.strftime('%H:%M:%S'),
        })
    return jsonify({'detections': detections, 'model_ready': model_ready})


@app.route('/analytics')
def analytics_page():
    return render_template('analytics.html')


@app.route('/api/growth_data')
def api_growth_data():
    """คืน JSON phenotype time-series ทุกขวด grouped by media_formula — ใช้กับ Chart.js"""
    FORMULA_LABEL = {
        'A': 'MS (control)',
        'B': 'MS + 1 BAP',
        'C': 'MS + 5 BAP',
        'D': 'MS + 5 BAP + 0.05 NAA',
        'E': 'MS + 1 IBA',
    }
    FORMULA_COLOR = {
        'A': 'rgb(148,163,184)',
        'B': 'rgb(251,191,36)',
        'C': 'rgb(34,197,94)',
        'D': 'rgb(99,102,241)',
        'E': 'rgb(249,115,22)',
    }

    rows = db.get_formulation_series()
    if not rows:
        return jsonify({'empty': True, 'metrics': {}, 'status': {}, 'formulas': []})

    import statistics as stat

    FORMULAS = ['A', 'B', 'C', 'D', 'E']
    METRICS  = ['vigor_score', 'green_coverage_pct', 'leaf_color_index',
                'brown_coverage_pct', 'texture_entropy', 'shoot_count_cv']

    # group by formula → day_point → list of values
    from collections import defaultdict
    raw = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for r in rows:
        f = r.get('media_formula') or _infer_formula(r['bottle_id'])
        d = r['day_point']
        for m in METRICS:
            v = r.get(m)
            if v is not None:
                raw[f][m][d].append(float(v))

    # aggregate: mean ± SE per formula per day
    metrics_out = {}
    for m in METRICS:
        all_days = sorted({d for f in raw for d in raw[f][m]})
        datasets = []
        for f in FORMULAS:
            means, ses, days_used = [], [], []
            for d in all_days:
                vals = raw[f][m].get(d, [])
                if not vals:
                    continue
                days_used.append(d)
                means.append(round(stat.mean(vals), 3))
                ses.append(round(stat.stdev(vals) / len(vals)**0.5 if len(vals) > 1 else 0, 3))
            if means:
                datasets.append({
                    'formula':  f,
                    'label':    FORMULA_LABEL.get(f, f),
                    'color':    FORMULA_COLOR.get(f, '#888'),
                    'days':     days_used,
                    'means':    means,
                    'ses':      ses,
                })
        metrics_out[m] = {'datasets': datasets}

    # status distribution (latest per bottle)
    latest_status = {}
    for r in rows:
        bid = r['bottle_id']
        if bid not in latest_status or r['day_point'] > latest_status[bid]['day']:
            latest_status[bid] = {'day': r['day_point'], 'status': r['status'],
                                  'formula': r.get('media_formula') or _infer_formula(bid)}

    status_counts = defaultdict(lambda: defaultdict(int))
    for v in latest_status.values():
        status_counts[v['formula']][v['status']] += 1

    status_out = {}
    for f in FORMULAS:
        status_out[f] = {
            'label':  FORMULA_LABEL.get(f, f),
            'color':  FORMULA_COLOR.get(f, '#888'),
            'counts': dict(status_counts[f]),
        }

    return jsonify({
        'empty':    False,
        'formulas': [{'key': f, 'label': FORMULA_LABEL.get(f, f),
                      'color': FORMULA_COLOR.get(f, '#888')} for f in FORMULAS],
        'metrics':  metrics_out,
        'status':   status_out,
    })


def _infer_formula(bottle_id):
    try:
        n = int(bottle_id[-3:] if len(bottle_id) >= 3 else bottle_id)
    except (ValueError, TypeError):
        return 'A'
    if n <= 20:  return 'A'
    if n <= 40:  return 'B'
    if n <= 60:  return 'C'
    if n <= 80:  return 'D'
    return 'E'


if __name__ == "__main__":
    db.init_db()
    app.run(debug=True, host="0.0.0.0", port=5001, use_reloader=False)
