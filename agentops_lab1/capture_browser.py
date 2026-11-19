import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path(r"C:\Users\vinod\OneDrive\Desktop\MLSDAP\agentops_lab1\deliverables")
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})

        # --- Screenshot 2: Web UI analysis ---
        page = context.new_page()
        page.goto("http://localhost:8000", wait_until="networkidle")
        page.wait_for_selector("#who:has-text('PES1UG25AM817')")
        
        sample_text = (
            "Docker packages an app with everything it needs. "
            "Containers start fast! Are they lighter than virtual machines? Yes."
        )
        page.fill("#task", sample_text)
        page.click("button:has-text('Analyze')")
        page.wait_for_selector("#result:has-text('Tools used:')", timeout=15000)
        time.sleep(1)
        page.screenshot(path=str(OUT_DIR / "screenshot_2_web_ui.png"))
        print("Captured screenshot_2_web_ui.png")

        # --- Screenshot 3: Swagger docs /health ---
        page.goto("http://localhost:8000/docs", wait_until="networkidle")
        time.sleep(1)
        # expand GET /health
        page.click("div.opblock-summary-get")
        time.sleep(0.5)
        # click Try it out
        page.click("button.try-out__btn")
        time.sleep(0.5)
        # click Execute
        page.click("button.execute")
        page.wait_for_selector("div.responses-wrapper:has-text('PES1UG25AM817')", timeout=10000)
        time.sleep(1)
        page.screenshot(path=str(OUT_DIR / "screenshot_3_health.png"))
        print("Captured screenshot_3_health.png")

        # --- Screenshot 7: Modification Task A (longest word) ---
        page.goto("http://localhost:8000", wait_until="networkidle")
        page.wait_for_selector("#who:has-text('PES1UG25AM817')")
        page.fill("#task", "Find the longest word: containers are wonderful")
        page.click("button:has-text('Analyze')")
        page.wait_for_selector("#result:has-text('find_longest_word')", timeout=15000)
        time.sleep(1)
        page.screenshot(path=str(OUT_DIR / "screenshot_7_mod_task_A_longest_word.png"))
        print("Captured screenshot_7_mod_task_A_longest_word.png")

        browser.close()

if __name__ == "__main__":
    run()
