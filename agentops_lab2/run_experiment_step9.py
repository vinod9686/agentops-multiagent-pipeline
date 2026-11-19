import subprocess
import time
import re
from pathlib import Path

ENV_PATH = Path(r"C:\Users\vinod\OneDrive\Desktop\MLSDAP\agentops_lab2\pipeline_lab_b\.env")
WORKDIR = Path(r"C:\Users\vinod\OneDrive\Desktop\MLSDAP\agentops_lab2\pipeline_lab_b")
PYTHON = Path(r"C:\Users\vinod\OneDrive\Desktop\MLSDAP\agentops_lab2\agent-env\Scripts\python.exe")

def set_max_retries(val):
    content = ENV_PATH.read_text()
    new_content = re.sub(r"MAX_RETRIES=\d+", f"MAX_RETRIES={val}", content)
    ENV_PATH.write_text(new_content)
    print(f"Set MAX_RETRIES={val} in .env")

def recreate_and_wait():
    print("Recreating containers with --force-recreate...")
    subprocess.run(["docker", "compose", "up", "-d", "--force-recreate"], cwd=WORKDIR, check=True)
    # Wait until all 4 healthy
    for _ in range(30):
        time.sleep(3)
        res = subprocess.run(["docker", "compose", "ps"], cwd=WORKDIR, capture_output=True, text=True)
        if res.stdout.count("(healthy)") >= 4:
            print("All 4 containers healthy!")
            return
    print("Warning: Timed out waiting for healthy containers.")

def run_batch_and_metrics(count=20):
    print(f"Running run_batch.py {count}...")
    subprocess.run([str(PYTHON), "run_batch.py", str(count)], cwd=WORKDIR, check=True)
    print(f"Running metrics.py --last {count}...")
    res = subprocess.run([str(PYTHON), "metrics.py", f"--last={count}"], cwd=WORKDIR, capture_output=True, text=True)
    print(res.stdout)
    return res.stdout

def main():
    results = {}
    for r in [0, 1, 3]:
        print(f"\n==================== TESTING MAX_RETRIES = {r} ====================")
        set_max_retries(r)
        recreate_and_wait()
        output = run_batch_and_metrics(20)
        results[r] = output
        time.sleep(2)

    # restore to 2
    set_max_retries(2)
    recreate_and_wait()

    # Save outputs to file
    out_file = Path(r"C:\Users\vinod\OneDrive\Desktop\MLSDAP\agentops_lab2\step9_results.txt")
    with out_file.open("w") as f:
        for r, out in results.items():
            f.write(f"\n--- RESULTS FOR MAX_RETRIES = {r} ---\n")
            f.write(out)
    print("Step 9 experiment finished! Saved to step9_results.txt")

if __name__ == "__main__":
    main()
