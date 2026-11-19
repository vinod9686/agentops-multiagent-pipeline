# run_batch.py -- sends many requests: python run_batch.py 10
import sys
import requests

TOPICS = [
    "docker", "langgraph", "fastapi", "agentops", "docker",
    "langgraph", "fastapi", "agentops", "docker", "kubernetes",
]
count = int(sys.argv[1]) if len(sys.argv) > 1 else 10

for i in range(count):
    topic = TOPICS[i % len(TOPICS)]
    try:
        resp = requests.post("http://localhost:8000/pipeline", json={"topic": topic}, timeout=60)
        r = resp.json()
        print(f"{i + 1:>3} {topic:<10} {r['status']:<9} retries={r['retries']} {r['latency_ms']} ms")
    except requests.RequestException as err:
        print(f"{i + 1:>3} {topic:<10} request error: {err}")

print(f"\nDone. Now run: python metrics.py --last {count}")
