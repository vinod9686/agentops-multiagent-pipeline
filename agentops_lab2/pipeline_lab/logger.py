# logger.py -- writes one JSON object per line (JSON Lines)
import json
import time
from pathlib import Path
import config

def log_event(**fields):
    path = Path(config.LOG_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"ts": round(time.time(), 3), **fields}
    with path.open("a") as f:
        f.write(json.dumps(record) + "\n")
