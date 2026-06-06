"""VitroVision Training UI — รันที่ port 5002"""
import json, time, threading
from pathlib import Path
from flask import Flask, render_template, Response, jsonify, request
from . import trainer

ROOT      = Path(__file__).parent.parent
DB_PATH   = ROOT / 'shelf_manager' / 'vitroshelf.db'
BASE_DIR  = ROOT / 'shelf_manager'
MODEL_OUT = ROOT / 'models' / 'final' / 'classifier.pt'

app = Flask(__name__, template_folder=str(Path(__file__).parent / 'train_templates'))

_log_buf: list  = []
_is_training    = False
_buf_lock       = threading.Lock()


def _on_log(data):
    with _buf_lock:
        _log_buf.append(data)


@app.route('/')
def index():
    stats = trainer.get_stats(DB_PATH, BASE_DIR)
    model_exists = MODEL_OUT.exists()
    return render_template('train.html', stats=stats, model_exists=model_exists)


@app.route('/api/stats')
def api_stats():
    return jsonify(trainer.get_stats(DB_PATH, BASE_DIR))


@app.route('/train', methods=['POST'])
def start_train():
    global _is_training, _log_buf
    if _is_training:
        return jsonify({'error': 'กำลัง train อยู่แล้ว'}), 400
    cfg = request.get_json(silent=True) or {}
    with _buf_lock:
        _log_buf = []
    _is_training = True

    def run():
        global _is_training
        trainer.run_training(DB_PATH, BASE_DIR, MODEL_OUT, cfg, _on_log)
        _is_training = False

    threading.Thread(target=run, daemon=True).start()
    return jsonify({'status': 'started'})


@app.route('/stop', methods=['POST'])
def stop_train():
    trainer.stop()
    return jsonify({'status': 'stopping'})


@app.route('/stream')
def stream():
    def generate():
        sent = 0
        while True:
            with _buf_lock:
                new = _log_buf[sent:]
                sent += len(new)
            for msg in new:
                yield f'data: {json.dumps(msg, ensure_ascii=False)}\n\n'
                if msg.get('type') in ('done', 'error'):
                    return
            time.sleep(0.4)
    return Response(generate(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})


if __name__ == '__main__':
    print(f'VitroVision Trainer — http://localhost:5002')
    app.run(host='0.0.0.0', port=5002, debug=False, threaded=True)
