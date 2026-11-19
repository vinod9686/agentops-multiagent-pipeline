# metrics.py -- turns logs/events.jsonl into the four AgentOps metrics
import argparse
import json
import math
from pathlib import Path
import requests
import config

parser = argparse.ArgumentParser()
parser.add_argument("--last", type=int, default=0, help="only the last N runs")
args = parser.parse_args()

path = Path(config.LOG_FILE)
if not path.exists():
    raise SystemExit("No log file yet. Run some pipelines first.")

events = [json.loads(line) for line in path.read_text().splitlines()]
runs = [e for e in events if e["event"] == "run"]
if args.last:
    runs = runs[-args.last:]
ids = {r["run_id"] for r in runs}
calls = [e for e in events if e["event"] == "call" and e["run_id"] in ids]
if not runs:
    raise SystemExit("No runs found in the log.")

total = len(runs)
count = lambda status: sum(1 for r in runs if r["status"] == status)
latencies = sorted(r["latency_ms"] for r in runs)
p95 = latencies[max(0, math.ceil(0.95 * total) - 1)]
first_tries = sum(1 for c in calls if c["attempt"] == 0)
retries = sum(1 for c in calls if c["attempt"] > 0)

print(f"=== Pipeline metrics ({total} runs) ===")
print(f"Task success rate      : {count('approved') / total * 100:.1f} %"
      f" (approved {count('approved')} of {total})")
print(f"  rejected by reviewer : {count('rejected')}")
print(f"  failed (service error): {count('failed')}")
print(f"Average run latency    : {sum(latencies) / total:.0f} ms")
print(f"95th percentile latency: {p95} ms")
retry_rate = retries / max(first_tries, 1) * 100
print(f"Retry rate             : {retry_rate:.1f} %"
      f" ({retries} retries / {first_tries} stage calls)")

print("--- Average successful call latency per stage ---")
for stage in ("researcher", "writer", "reviewer"):
    ok = [c["latency_ms"] for c in calls if c["stage"] == stage and c["ok"]]
    if ok:
        avg = sum(ok) / len(ok)
        print(f"  {stage:<11}: {avg:.0f} ms ({len(ok)} calls)")

print("--- Container uptime (from /services) ---")
try:
    url = "http://localhost:8000/services"
    report = requests.get(url, timeout=3).json()
    for name, info in report.items():
        state = "UP" if info["up"] else "DOWN"
        mins, secs = divmod(info["uptime_s"], 60)
        print(f"  {name:<11}: {state} {mins} min {secs} s")
except requests.RequestException:
    print("  (orchestrator is not reachable on localhost:8000)")
