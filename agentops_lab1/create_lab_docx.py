import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from pathlib import Path

DELIV_DIR = Path(r"C:\Users\vinod\OneDrive\Desktop\MLSDAP\agentops_lab1\deliverables")
DOCX_PATH = DELIV_DIR / "PES1UG25AM817_Unit4_Lab1_Deliverables.docx"
SRN = "PES1UG25AM817"
STUDENT_NAME = "Vinod"

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout(doc, text, title="NOTE"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run_t = p.add_run(f"[{title}] ")
    run_t.bold = True
    run_t.font.color.rgb = RGBColor(27, 85, 155)
    run_txt = p.add_run(text)
    run_txt.font.size = Pt(10)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "1E1E1E")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(code_str.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(220, 220, 220)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_docx():
    doc = Document()

    # Page Margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Header section
    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_hdr = p_header.add_run("Dept of CSE (AI & ML), PESU, RR Campus")
    r_hdr.font.size = Pt(9)
    r_hdr.font.color.rgb = RGBColor(120, 120, 120)

    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    run_title = p_title.add_run("Unit 4 Hands-On Activity 1\nHosting, Consuming and Containerizing an AI Agent")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(18)
    run_title.bold = True
    run_title.font.color.rgb = RGBColor(30, 60, 114)

    # Subtitle / Course
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(12)
    run_sub = p_sub.add_run("B.Tech CSE (AI & ML) — ML System Design and AgentOps Lab Manual\nPractice & Submission Deliverables Report")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(12)
    run_sub.font.color.rgb = RGBColor(70, 70, 70)

    # Student metadata table
    tbl_meta = doc.add_table(rows=4, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Student Name:", STUDENT_NAME),
        ("Student SRN:", SRN),
        ("Course / Department:", "B.Tech CSE (AI & ML) — PES University"),
        ("Date of Completion:", "November 19, 2026")
    ]
    for i, (k, v) in enumerate(meta_data):
        cell_k = tbl_meta.cell(i, 0)
        cell_v = tbl_meta.cell(i, 1)
        set_cell_background(cell_k, "EAECEE")
        set_cell_background(cell_v, "F8F9F9")
        set_cell_margins(cell_k, top=60, bottom=60, left=100, right=100)
        set_cell_margins(cell_v, top=60, bottom=60, left=100, right=100)
        pk = cell_k.paragraphs[0]
        rk = pk.add_run(k)
        rk.bold = True
        rk.font.size = Pt(10)
        pv = cell_v.paragraphs[0]
        rv = pv.add_run(v)
        rv.font.size = Pt(10)
        if k == "Student SRN:":
            rv.bold = True
            rv.font.color.rgb = RGBColor(180, 40, 40)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- Section 1: Overview & Syllabus ---
    h1 = doc.add_heading(level=1)
    r = h1.add_run("1. Syllabus Topics & Objectives")
    r.font.color.rgb = RGBColor(30, 60, 114)

    p = doc.add_paragraph()
    p.add_run("Syllabus Topics Covered: ").bold = True
    p.add_run(
        "Strategies for consuming AI agents: hosting agents through REST APIs using FastAPI, and consuming "
        "agent web services through web applications. Containerization of agent systems using Docker: "
        "Dockerizing agent microservices and managing dependencies. Externalizing agent microservices: "
        "environment configuration, secrets management and deployment strategies."
    )

    p_obj = doc.add_paragraph()
    p_obj.add_run("Laboratory Objectives:").bold = True
    bullets = [
        "Construct a modular AI agent using LangGraph with a stateful tool-calling graph loop.",
        "Expose the agent as a REST API microservice using FastAPI with /health, /run, and root web interface endpoints.",
        "Package the microservice into an immutable Docker image with optimized layer caching for Python dependencies.",
        "Externalize runtime configuration and credentials (.env, STUDENT_SRN, GROQ_API_KEY) to ensure zero code modification upon reconfiguration.",
        "Demonstrate dynamic reconfiguration without rebuilding the image using alternate environment variables."
    ]
    for b in bullets:
        bp = doc.add_paragraph(style='List Bullet')
        bp.add_run(b)

    # --- Section 2: Architecture & Data Flow Diagram ---
    h2 = doc.add_heading(level=1)
    r = h2.add_run("2. System Architecture & Agent Flow Diagram")
    r.font.color.rgb = RGBColor(30, 60, 114)

    p_diag_intro = doc.add_paragraph(
        "Below is the complete system architecture diagram illustrating the interaction between the Client Web Browser, "
        "the FastAPI REST container service, the LangGraph execution loop, externalized configuration, and the cloud LLM inference engine:"
    )

    diagram_path = DELIV_DIR / f"{SRN}_agent_flow.png"
    if diagram_path.exists():
        doc.add_picture(str(diagram_path), width=Inches(6.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rc = p_cap.add_run(f"Figure 1: Complete System Architecture & Agent Data Flow Diagram ({SRN})")
        rc.italic = True
        rc.font.size = Pt(9.5)

    add_callout(doc, "The architecture strictly decouples the client interface, REST API routing, agent orchestration, and LLM provider. The Docker container receives runtime identity and API secrets via host injection (--env-file).", "ARCHITECTURAL PRINCIPLE")

    # --- Section 3: Implementation Code Listing ---
    h3 = doc.add_heading(level=1)
    r = h3.add_run("3. Source Code Implementation (text_agent)")
    r.font.color.rgb = RGBColor(30, 60, 114)

    doc.add_heading("3.1 Externalized Configuration (.env.submit & config.py)", level=2)
    doc.add_paragraph("Configuration file with masked secret (never commit real secrets):")
    add_code_block(doc, """GROQ_API_KEY=xxxx
STUDENT_SRN=PES1UG25AM817
MODEL_NAME=qwen/qwen3.8-27b
TEMPERATURE=0
SYSTEM_PROMPT=You are a text-analysis assistant. When the user gives you text, always call the analyze_text tool with that exact text, then explain the results in two sentences.
USE_MOCK_LLM=false
MAX_INPUT_CHARS=2000""")

    doc.add_paragraph("config.py -- Centralized environment loader:")
    add_code_block(doc, """import os
from dotenv import load_dotenv

load_dotenv()

STUDENT_SRN = os.getenv("STUDENT_SRN", "UNKNOWN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen/qwen3.8-27b")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "false").lower() == "true"
MAX_INPUT_CHARS = int(os.getenv("MAX_INPUT_CHARS", "2000"))""")

    doc.add_heading("3.2 Tools Definition (tools.py)", level=2)
    doc.add_paragraph("Contains primary tool analyze_text and secondary tool find_longest_word:")
    add_code_block(doc, """import re
from langchain_core.tools import tool

@tool
def analyze_text(text: str) -> str:
    \"\"\"Analyze a piece of text and report its word count, sentence count, character count and reading time.\"\"\"
    words = text.split()
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    minutes = len(words) / 200
    return f"Words: {len(words)}, Sentences: {len(sentences)}, Characters: {len(text)}, Reading time: {minutes:.1f} min"

@tool
def find_longest_word(text: str) -> str:
    \"\"\"Find and return the longest word in the text.\"\"\"
    words = re.findall(r"\\b\\w+\\b", text)
    if not words:
        return "No words found."
    longest = max(words, key=len)
    return f"Longest word: '{longest}' ({len(longest)} characters)\"""")

    doc.add_heading("3.3 Agent Workflow (agent.py)", level=2)
    add_code_block(doc, """from langchain_core.messages import SystemMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
import config
from llm import get_llm
from tools import analyze_text, find_longest_word

TOOLS = [analyze_text, find_longest_word]

def mock_router(text):
    if "longest" in text.lower():
        return "find_longest_word", {"text": text}
    return "analyze_text", {"text": text}

llm = get_llm(mock_router).bind_tools(TOOLS)

def agent_node(state: MessagesState):
    messages = [SystemMessage(content=config.SYSTEM_PROMPT)] + state["messages"]
    return {"messages": [llm.invoke(messages)]}

builder = StateGraph(MessagesState)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(TOOLS))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
graph = builder.compile()""")

    doc.add_heading("3.4 FastAPI REST API Microservice (main.py)", level=2)
    add_code_block(doc, """import time
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from langchain_core.messages import HumanMessage, ToolMessage
from pydantic import BaseModel
import config
from agent import graph

app = FastAPI(title="Text Helper Agent")

class RunRequest(BaseModel):
    task: str

@app.get("/health")
def health():
    return {
        "status": "ok",
        "student": config.STUDENT_SRN,
        "model": config.MODEL_NAME,
        "mock_llm": config.USE_MOCK_LLM,
    }

@app.post("/run")
def run(req: RunRequest):
    if len(req.task) > config.MAX_INPUT_CHARS:
        raise HTTPException(
            status_code=400,
            detail=f"Task exceeds maximum allowed length of {config.MAX_INPUT_CHARS} characters (received {len(req.task)})."
        )
    start = time.perf_counter()
    inputs = {"messages": [HumanMessage(content=req.task)]}
    try:
        result = graph.invoke(inputs)
    except Exception as err:
        raise HTTPException(status_code=502, detail=f"Agent failed: {err}")
    messages = result["messages"]
    tools_used = [m.name for m in messages if isinstance(m, ToolMessage)]
    return {
        "student": config.STUDENT_SRN,
        "answer": messages[-1].content,
        "tools_used": tools_used,
        "model": config.MODEL_NAME,
        "latency_ms": round((time.perf_counter() - start) * 1000),
    }

@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "static" / "index.html")""")

    doc.add_heading("3.5 Dockerfile & .dockerignore", level=2)
    add_code_block(doc, """# Dockerfile
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# .dockerignore
.env
.env.*
__pycache__
*.pyc""")

    # --- Section 4: Screenshots & Outputs ---
    h4 = doc.add_heading(level=1)
    r = h4.add_run("4. Execution Outputs & Verification Screenshots")
    r.font.color.rgb = RGBColor(30, 60, 114)

    shots = [
        ("Screenshot 1: Local Uvicorn Server Startup", "screenshot_1_uvicorn_local.png",
         "Local testing of FastAPI uvicorn server in PowerShell prior to containerization."),
        ("Screenshot 2: Web Application Running in Browser", "screenshot_2_web_ui.png",
         "Web UI at http://localhost:8000 showing student identification (PES1UG25AM817), model name, text metrics, and tool used."),
        ("Screenshot 3: Health Check REST Endpoint (GET /health)", "screenshot_3_health.png",
         "Health check JSON response confirming container status, student SRN attribution, and active model."),
        ("Screenshot 4: Docker Image Build & Container Run", "screenshot_4_docker_build_run.png",
         "Building image student-agent:PES1UG25AM817 with cached dependency layers and executing with host port forwarding (-p 8000:8000)."),
        ("Screenshot 5: Docker Images Repository", "screenshot_5_docker_images.png",
         "Local Docker image cache displaying base python:3.11-slim, student-agent, and versioned tags."),
        ("Screenshot 6: Docker Running Containers (docker ps)", "screenshot_6_docker_ps.png",
         "Verification of active student-agent container with port binding 0.0.0.0:8000->8000/tcp."),
        ("Screenshot 7: Modification Task A — Longest Word Tool", "screenshot_7_mod_task_A_longest_word.png",
         "Invocation and execution of the find_longest_word tool with test prompt 'Find the longest word: containers are wonderful'."),
        ("Screenshot 8: Modification Task B — Guardrail Length Refusal (HTTP 400)", "screenshot_8_mod_task_B_refusal_400.png",
         "Demonstrating HTTP 400 Bad Request refusal when user prompt exceeds configured threshold (MAX_INPUT_CHARS=50).")
    ]

    for title, fname, caption in shots:
        doc.add_heading(title, level=2)
        p_desc = doc.add_paragraph(caption)
        fpath = DELIV_DIR / fname
        if fpath.exists():
            doc.add_picture(str(fpath), width=Inches(6.2))
            p_c = doc.add_paragraph()
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            rc = p_c.add_run(caption)
            rc.italic = True
            rc.font.size = Pt(9)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # --- Section 5: Modification Task Analysis ---
    h5 = doc.add_heading(level=1)
    r = h5.add_run("5. Student Modification Task Analysis")
    r.font.color.rgb = RGBColor(30, 60, 114)

    tbl_tasks = doc.add_table(rows=3, cols=4)
    tbl_tasks.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Task", "Type of Change", "Rebuild Required?", "Technical Reason"]
    for j, h in enumerate(headers):
        cell = tbl_tasks.cell(0, j)
        set_cell_background(cell, "2B579A")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(9.5)

    task_rows = [
        ("Part A: find_longest_word tool", "Source Code (.py)", "YES",
         "Adding tools modifies tools.py and agent.py. Because Python source code is baked into the image at build time (COPY . .), changing code requires 'docker build'."),
        ("Part B: MAX_INPUT_CHARS limit", "Runtime Config (.env)", "NO (after v2 code)",
         "Environment variables are injected at runtime via '--env-file'. os.getenv reads values when the container starts, requiring only a restart without rebuilding.")
    ]
    for i, row in enumerate(task_rows):
        for j, val in enumerate(row):
            cell = tbl_tasks.cell(i + 1, j)
            set_cell_background(cell, "F2F4F7" if i % 2 == 0 else "FFFFFF")
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if j == 2:
                r.bold = True
                r.font.color.rgb = RGBColor(180, 0, 0) if val == "YES" else RGBColor(0, 120, 0)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- Section 6: Viva Questions ---
    h6 = doc.add_heading(level=1)
    r = h6.add_run("6. Viva Voce Questions & Detailed Answers")
    r.font.color.rgb = RGBColor(30, 60, 114)

    viva = [
        ("Q1: Which parts of your project stayed the same as Experiment 1A, and which had to change for the new agent? What does that tell you about the architecture?",
         "Answer: llm.py, Dockerfile, .dockerignore, requirements.txt, and the StateGraph compilation loop in agent.py stayed exactly the same. Only tools.py and specific prompt/SRN keys in .env changed. This demonstrates that the microservice agent architecture is decoupled, reusable, and modular."),

        ("Q2: In Step 10 you changed the model, temperature and prompt without rebuilding. Why was that possible? Which kind of change always needs a rebuild?",
         "Answer: It was possible because configuration settings are externalized using environment variables loaded at runtime (load_dotenv() locally and --env-file in Docker). Changes to configuration never require a rebuild. Changes to executable application source code (.py files), HTML templates, or installed pip libraries alter the filesystem layers and always require a rebuild (docker build)."),

        ("Q3: What does tools_used in the response tell you about what the agent did?",
         "Answer: tools_used inspects the LangGraph state for ToolMessage instances. It provides observability into whether the LLM decided to invoke an external function (e.g. analyze_text) or whether it answered directly from its parametric weights without tool augmentation."),

        ("Q4: Why is your SRN passed as an environment variable rather than typed into main.py?",
         "Answer: Passing STUDENT_SRN as an environment variable decouples identity from source code. This follows 12-factor application methodology, allowing the exact same immutable container image to be deployed for any student or user without code modifications or recompilation."),

        ("Q5: What happens if you start two containers that both map host port 8000? How would you run both at the same time?",
         "Answer: The second container fails to start with the error 'port is already allocated' because only one host process can bind to a given TCP port. To run both concurrently, map different host ports to container port 8000: e.g., container 1 on -p 8000:8000 and container 2 on -p 8001:8000."),

        ("Q6: Why does the Dockerfile copy requirements.txt and install packages before copying the rest of the code?",
         "Answer: Docker caches build steps layer by layer. Package installations (pip install) are slow and change infrequently. By isolating requirements.txt in its own layer before COPY . ., Docker reuses the cached layer on subsequent builds, reducing rebuild time from minutes to milliseconds.")
    ]

    for q, a in viva:
        doc.add_heading(q, level=3)
        pa = doc.add_paragraph()
        ra = pa.add_run(a)
        ra.font.size = Pt(10)
        pa.paragraph_format.space_after = Pt(6)

    doc.save(str(DOCX_PATH))
    print(f"Successfully generated deliverable DOCX: {DOCX_PATH}")

if __name__ == "__main__":
    build_docx()
