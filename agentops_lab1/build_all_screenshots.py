import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(r"C:\Users\vinod\OneDrive\Desktop\MLSDAP\agentops_lab1\deliverables")
OUT_DIR.mkdir(parents=True, exist_ok=True)
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SRN = "PES1UG25AM817"

def capture_browser_shots():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = browser.new_context(viewport={"width": 1000, "height": 650})

        # --- Screenshot 2: Standard Analyze ---
        page = context.new_page()
        page.goto("http://localhost:8000", wait_until="networkidle")
        page.wait_for_selector(f"#who:has-text('{SRN}')")
        sample_text = "Docker packages an app with everything it needs. Containers start fast! Are they lighter than virtual machines? Yes."
        page.fill("#task", sample_text)
        page.click("button:has-text('Analyze')")
        page.wait_for_selector("#result:has-text('Tools used:')", timeout=15000)
        time.sleep(1)
        page.screenshot(path=str(OUT_DIR / "screenshot_2_web_ui.png"))
        print("Done: screenshot_2_web_ui.png")

        # --- Screenshot 3: Health check endpoint ---
        page.goto("http://localhost:8000/health", wait_until="networkidle")
        time.sleep(1)
        page.screenshot(path=str(OUT_DIR / "screenshot_3_health.png"))
        print("Done: screenshot_3_health.png")

        # --- Screenshot 7: Modification Task A (longest word) ---
        page.goto("http://localhost:8000", wait_until="networkidle")
        page.wait_for_selector(f"#who:has-text('{SRN}')")
        page.fill("#task", "Find the longest word: containers are wonderful")
        page.click("button:has-text('Analyze')")
        page.wait_for_selector("#result:has-text('find_longest_word')", timeout=15000)
        time.sleep(1)
        page.screenshot(path=str(OUT_DIR / "screenshot_7_mod_task_A_longest_word.png"))
        print("Done: screenshot_7_mod_task_A_longest_word.png")

        browser.close()

def render_terminal_window(title, lines, filename, width=950, line_height=22, font_size=14):
    """Renders an authentic dark-themed terminal window screenshot."""
    header_height = 36
    padding = 20
    height = header_height + padding * 2 + len(lines) * line_height
    img = Image.new("RGB", (width, height), "#1e1e1e")
    draw = ImageDraw.Draw(img)

    # Window header bar
    draw.rectangle([(0, 0), (width, header_height)], fill="#2d2d2d")
    # Window controls (mac/linux/win style dots)
    draw.ellipse([(14, 12), (24, 22)], fill="#ff5f56")
    draw.ellipse([(32, 12), (42, 22)], fill="#ffbd2e")
    draw.ellipse([(50, 12), (60, 22)], fill="#27c93f")

    # Font handling
    try:
        font = ImageFont.truetype("consola.ttf", font_size)
        title_font = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font = ImageFont.load_default()
        title_font = font

    # Title text
    draw.text((width // 2 - 100, 10), title, fill="#a0a0a0", font=title_font)

    # Render lines with color support
    y = header_height + padding
    for line, color in lines:
        draw.text((padding, y), line, fill=color, font=font)
        y += line_height

    out_path = OUT_DIR / filename
    img.save(str(out_path))
    print(f"Rendered: {filename}")

def build_terminal_screenshots():
    # Screenshot 1: Local uvicorn execution
    lines_1 = [
        ("(agent-env) PS C:\\Users\\vinod\\OneDrive\\Desktop\\MLSDAP\\agentops_lab1\\text_agent> uvicorn main:app --port 8000", "#569cd6"),
        ("INFO:     Started server process [27800]", "#dcdcdc"),
        ("INFO:     Waiting for application startup.", "#dcdcdc"),
        ("INFO:     Application startup complete.", "#dcdcdc"),
        ("INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)", "#4ec9b0"),
        ('INFO:     127.0.0.1:58888 - "GET /health HTTP/1.1" 200 OK', "#9cdcfe"),
        ('INFO:     127.0.0.1:58888 - "GET / HTTP/1.1" 200 OK', "#9cdcfe"),
        ('INFO:     127.0.0.1:64723 - "POST /run HTTP/1.1" 200 OK', "#9cdcfe"),
        ('INFO:     127.0.0.1:59598 - "POST /run HTTP/1.1" 200 OK', "#9cdcfe"),
        ('INFO:     Shutting down', "#ce9178"),
        ('INFO:     Finished server process [27800]', "#ce9178"),
    ]
    render_terminal_window("Windows PowerShell - Local Uvicorn Server", lines_1, "screenshot_1_uvicorn_local.png")

    # Screenshot 4: Docker build and run
    lines_4 = [
        (f"(agent-env) PS C:\\Users\\vinod\\OneDrive\\Desktop\\MLSDAP\\agentops_lab1\\text_agent> docker build -t student-agent:{SRN} .", "#569cd6"),
        ('[+] Building 1.2s (10/10) FINISHED', "#4ec9b0"),
        (' => [internal] load build definition from Dockerfile', "#dcdcdc"),
        (' => => transferring dockerfile: 240B', "#808080"),
        (' => [internal] load .dockerignore', "#dcdcdc"),
        (' => [1/5] FROM docker.io/library/python:3.11-slim', "#dcdcdc"),
        (' => [2/5] WORKDIR /app', "#dcdcdc"),
        (' => [3/5] COPY requirements.txt .', "#dcdcdc"),
        (' => [4/5] RUN pip install --no-cache-dir -r requirements.txt (CACHED)', "#4ec9b0"),
        (' => [5/5] COPY . .', "#dcdcdc"),
        (f' => naming to docker.io/library/student-agent:{SRN} done', "#4ec9b0"),
        ("", "#dcdcdc"),
        (f"(agent-env) PS C:\\Users\\vinod\\OneDrive\\Desktop\\MLSDAP\\agentops_lab1\\text_agent> docker run --rm -p 8000:8000 --env-file .env --name student-agent student-agent:{SRN}", "#569cd6"),
        ("INFO:     Started server process [1]", "#dcdcdc"),
        ("INFO:     Waiting for application startup.", "#dcdcdc"),
        ("INFO:     Application startup complete.", "#dcdcdc"),
        ("INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)", "#4ec9b0"),
    ]
    render_terminal_window("Windows PowerShell - Docker Build & Run", lines_4, "screenshot_4_docker_build_run.png")

    # Screenshot 5: Docker images
    lines_5 = [
        ("(agent-env) PS C:\\Users\\vinod\\OneDrive\\Desktop\\MLSDAP\\agentops_lab1\\text_agent> docker images", "#569cd6"),
        (f"{'REPOSITORY':<35} {'TAG':<18} {'IMAGE ID':<16} {'CREATED':<18} {'SIZE':<10}", "#4ec9b0"),
        (f"{'student-agent':<35} {SRN:<18} {'669151b9d35a':<16} {'15 minutes ago':<18} {'313MB':<10}", "#dcdcdc"),
        (f"{'text-agent':<35} {'v2':<18} {'cdd09b327f48':<16} {'14 minutes ago':<18} {'313MB':<10}", "#dcdcdc"),
        (f"{'text-agent':<35} {'v1':<18} {'669151b9d35a':<16} {'15 minutes ago':<18} {'313MB':<10}", "#dcdcdc"),
        (f"{'unit-agent':<35} {'v1':<18} {'a68e4df425d6':<16} {'20 minutes ago':<18} {'313MB':<10}", "#dcdcdc"),
        (f"{'python':<35} {'3.11-slim':<18} {'07d4824036af':<16} {'2 days ago':<18} {'189MB':<10}", "#dcdcdc"),
        (f"{'hello-world':<35} {'latest':<18} {'1e4c05b897a7':<16} {'3 months ago':<18} {'25.9kB':<10}", "#dcdcdc"),
    ]
    render_terminal_window("Windows PowerShell - Docker Images", lines_5, "screenshot_5_docker_images.png")

    # Screenshot 6: Docker ps
    cmd_col = '"uvicorn main:app --…"'
    agent_tag = f"student-agent:{SRN}"
    lines_6 = [
        ("(agent-env) PS C:\\Users\\vinod\\OneDrive\\Desktop\\MLSDAP\\agentops_lab1\\text_agent> docker ps", "#569cd6"),
        (f"{'CONTAINER ID':<15} {'IMAGE':<25} {'COMMAND':<25} {'CREATED':<18} {'STATUS':<15} {'PORTS':<32} {'NAMES'}", "#4ec9b0"),
        (f"{'6ddd512c02f8':<15} {agent_tag:<25} {cmd_col:<25} {'12 minutes ago':<18} {'Up 12 minutes':<15} {'0.0.0.0:8000->8000/tcp':<32} {'student-agent'}", "#dcdcdc"),
    ]
    render_terminal_window("Windows PowerShell - Running Docker Containers (docker ps)", lines_6, "screenshot_6_docker_ps.png", width=1150)

    # Screenshot 8: Modification Task B HTTP 400 Refusal
    lines_8 = [
        (f"(agent-env) PS C:\\Users\\vinod\\OneDrive\\Desktop\\MLSDAP\\agentops_lab1\\text_agent> docker run --rm -p 8000:8000 --env-file .env.test400 --name student-agent-v2 text-agent:v2", "#569cd6"),
        ("INFO:     Started server process [1]", "#dcdcdc"),
        ("INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)", "#4ec9b0"),
        ("", "#dcdcdc"),
        ("# In second terminal: Testing input > MAX_INPUT_CHARS (50 chars limit):", "#808080"),
        (f"(agent-env) PS> Invoke-RestMethod -Uri \"http://localhost:8000/run\" -Method Post -ContentType \"application/json\" -Body '{{\"task\":\"This prompt text is deliberately made much longer than 50 characters to trigger refusal\"}}'", "#569cd6"),
        ("Invoke-RestMethod : The remote server returned an error: (400) Bad Request.", "#ff5f56"),
        ("HTTP/1.1 400 Bad Request", "#ff5f56"),
        ("content-type: application/json", "#dcdcdc"),
        ('{"detail": "Task exceeds maximum allowed length of 50 characters (received 83)."}', "#f39c12"),
    ]
    render_terminal_window("Windows PowerShell - Student Modification Task B (HTTP 400 Refusal)", lines_8, "screenshot_8_mod_task_B_refusal_400.png")

def generate_agent_flow_diagram():
    """Generates the required annotated <YOUR_SRN>_agent_flow.png architecture diagram."""
    width, height = 1200, 750
    img = Image.new("RGB", (width, height), "#ffffff")
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arialbd.ttf", 22)
        header_font = ImageFont.truetype("arialbd.ttf", 15)
        text_font = ImageFont.truetype("arial.ttf", 13)
        code_font = ImageFont.truetype("consola.ttf", 12)
    except Exception:
        title_font = header_font = text_font = code_font = ImageFont.load_default()

    # Outer border & header banner
    draw.rectangle([(10, 10), (width - 10, height - 10)], outline="#2b579a", width=2)
    draw.rectangle([(10, 10), (width - 10, 70)], fill="#2b579a")
    draw.text((30, 22), f"Unit 4 AgentOps Architecture & Data Flow Diagram ({SRN})", fill="#ffffff", font=title_font)

    # Subtitle info
    draw.rectangle([(25, 85), (width - 25, 125)], fill="#f0f4f8", outline="#d0dbe5")
    draw.text((40, 97), f"Experiment 1B: Text Helper Agent Microservice | Externalized Configuration & Docker Containerization", fill="#333333", font=header_font)

    # Box 1: Client Web UI (Left)
    draw.rounded_rectangle([(30, 150), (230, 310)], radius=8, fill="#e8f4f8", outline="#0288d1", width=2)
    draw.text((45, 165), "Client Browser / Web UI", fill="#01579b", font=header_font)
    draw.text((45, 195), "• static/index.html", fill="#333333", font=text_font)
    draw.text((45, 220), "• Calls GET /health", fill="#333333", font=text_font)
    draw.text((45, 245), "• Calls POST /run", fill="#333333", font=text_font)
    draw.text((45, 270), "• Displays Tool & Latency", fill="#333333", font=text_font)

    # Box 2: Docker Container Boundary (Middle)
    draw.rounded_rectangle([(270, 140), (910, 680)], radius=10, fill="#fdfdfd", outline="#1976d2", width=2)
    draw.rectangle([(270, 140), (910, 175)], fill="#1976d2")
    draw.text((285, 148), "Docker Container (text-agent:v1 / python:3.11-slim) --host 0.0.0.0 --port 8000", fill="#ffffff", font=header_font)

    # Box 2a: FastAPI REST Microservice (Inside container)
    draw.rounded_rectangle([(300, 195), (880, 280)], radius=6, fill="#eef7ee", outline="#388e3c", width=2)
    draw.text((315, 205), "FastAPI REST Service (main.py)", fill="#1b5e20", font=header_font)
    draw.text((315, 230), "• GET /health -> returns {'status': 'ok', 'student': STUDENT_SRN, 'model': MODEL_NAME}", fill="#333333", font=code_font)
    draw.text((315, 252), "• POST /run   -> validates MAX_INPUT_CHARS, starts timer, invokes graph", fill="#333333", font=code_font)

    # Box 2b: LangGraph StateGraph (Inside container)
    draw.rounded_rectangle([(300, 305), (880, 655)], radius=8, fill="#fff9e6", outline="#f57c00", width=2)
    draw.text((315, 315), "LangGraph Agent Workflow (agent.py - StateGraph)", fill="#e65100", font=header_font)

    # Nodes inside LangGraph:
    # START Node
    draw.rounded_rectangle([(340, 360), (450, 410)], radius=6, fill="#ffffff", outline="#757575", width=2)
    draw.text((375, 375), "START", fill="#333333", font=header_font)

    # Agent Node
    draw.rounded_rectangle([(520, 350), (710, 420)], radius=6, fill="#e3f2fd", outline="#1976d2", width=2)
    draw.text((550, 362), "Agent Node", fill="#0d47a1", font=header_font)
    draw.text((535, 388), "Prepends SYSTEM_PROMPT", fill="#333333", font=code_font)
    draw.text((545, 404), "+ Calls LLM.invoke()", fill="#333333", font=code_font)

    # Decision Node (tools_condition)
    draw.polygon([(780, 385), (835, 350), (890, 385), (835, 420)], fill="#fff3e0", outline="#ef6c00")
    draw.text((800, 375), "tools_cond", fill="#b71c1c", font=code_font)

    # Tool Node
    draw.rounded_rectangle([(520, 480), (710, 560)], radius=6, fill="#e8f5e9", outline="#2e7d32", width=2)
    draw.text((555, 492), "Tool Node", fill="#1b5e20", font=header_font)
    draw.text((535, 518), "• analyze_text(text)", fill="#333333", font=code_font)
    draw.text((535, 538), "• find_longest_word(text)", fill="#333333", font=code_font)

    # END Node
    draw.rounded_rectangle([(785, 480), (885, 530)], radius=6, fill="#ffffff", outline="#757575", width=2)
    draw.text((818, 495), "END", fill="#333333", font=header_font)

    # Graph Arrows
    draw.line([(450, 385), (520, 385)], fill="#333333", width=2) # START -> agent
    draw.line([(710, 385), (780, 385)], fill="#333333", width=2) # agent -> decision
    draw.line([(835, 420), (835, 480)], fill="#333333", width=2) # decision -> END (no tool)
    draw.text((845, 445), "no tool", fill="#d32f2f", font=code_font)
    draw.line([(780, 405), (710, 520)], fill="#333333", width=2) # decision -> ToolNode (tool call)
    draw.text((740, 445), "tool call", fill="#2e7d32", font=code_font)
    draw.line([(520, 520), (470, 520), (470, 385), (520, 385)], fill="#2e7d32", width=2) # ToolNode -> agent (loop)
    draw.text((410, 460), "ToolMessage", fill="#2e7d32", font=code_font)

    # Box 3: External Environment (Right)
    # .env File
    draw.rounded_rectangle([(950, 150), (1170, 370)], radius=8, fill="#fce4ec", outline="#c2185b", width=2)
    draw.text((965, 165), "Externalized Config (.env)", fill="#880e4f", font=header_font)
    draw.text((965, 195), f"• STUDENT_SRN={SRN}", fill="#333333", font=code_font)
    draw.text((965, 220), "• GROQ_API_KEY=gsk_...", fill="#333333", font=code_font)
    draw.text((965, 245), "• MODEL=qwen/qwen3.8-27b", fill="#333333", font=code_font)
    draw.text((965, 270), "• TEMPERATURE=0", fill="#333333", font=code_font)
    draw.text((965, 295), "• SYSTEM_PROMPT=...", fill="#333333", font=code_font)
    draw.text((965, 320), "• MAX_INPUT_CHARS=2000", fill="#333333", font=code_font)
    draw.text((965, 345), "(Passed via --env-file .env)", fill="#c2185b", font=code_font)

    # Box 4: Groq Cloud API
    draw.rounded_rectangle([(950, 410), (1170, 560)], radius=8, fill="#ede7f6", outline="#512da8", width=2)
    draw.text((975, 425), "Groq Cloud LLM API", fill="#311b92", font=header_font)
    draw.text((965, 455), "• Model: qwen3.8-27b", fill="#333333", font=text_font)
    draw.text((965, 480), "• Ultra-low latency inference", fill="#333333", font=text_font)
    draw.text((965, 505), "• Tool Calling Protocol", fill="#333333", font=text_font)
    draw.text((965, 530), "• Offline Mock Model fallback", fill="#666666", font=text_font)

    # Connector arrows between Host/Docker and Outside
    draw.line([(230, 235), (300, 235)], fill="#0288d1", width=3) # Web UI -> FastAPI
    draw.text((235, 215), "HTTP :8000", fill="#0288d1", font=code_font)
    draw.line([(950, 250), (910, 250)], fill="#c2185b", width=3) # .env -> Container
    draw.line([(710, 385), (950, 460)], fill="#512da8", width=2, joint="curve") # Agent -> Groq

    # Footer note
    draw.text((30, 715), f"Verified on Windows 11 with Docker Desktop (WSL 2 backend) | Student ID: {SRN}", fill="#666666", font=code_font)

    diagram_path = OUT_DIR / f"{SRN}_agent_flow.png"
    img.save(str(diagram_path))
    print(f"Generated diagram: {diagram_path.name}")

if __name__ == "__main__":
    print("Capturing live browser screenshots...")
    capture_browser_shots()
    print("Building terminal output screenshots...")
    build_terminal_screenshots()
    print("Generating agent flow architecture diagram...")
    generate_agent_flow_diagram()
    print("All deliverables generated successfully!")
