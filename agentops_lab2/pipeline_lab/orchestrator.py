# orchestrator.py -- runs researcher -> writer -> reviewer safely
import time
import uuid
from pathlib import Path
from typing import TypedDict
import requests
from fastapi import FastAPI
from fastapi.responses import FileResponse
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel
import config
from logger import log_event

STARTED = time.time()
URLS = {
    "researcher": config.RESEARCHER_URL,
    "writer": config.WRITER_URL,
    "reviewer": config.REVIEWER_URL,
}

class StageError(Exception):
    """Raised when a stage still fails after all its retries."""
    def __init__(self, stage, reason, retries):
        super().__init__(f"{stage}: {reason}")
        self.stage, self.reason, self.retries = stage, reason, retries

def call_agent(run_id, stage, text):
    """Call one agent. Returns (output, retries_used)."""
    for attempt in range(config.MAX_RETRIES + 1):
        began = time.perf_counter()
        try:
            resp = requests.post(
                URLS[stage] + "/run",
                json={"text": text},
                timeout=config.TIMEOUT_S,
            )
            resp.raise_for_status()
            ms = round((time.perf_counter() - began) * 1000)
            log_event(event="call", run_id=run_id, stage=stage, attempt=attempt, ok=True, latency_ms=ms)
            return resp.json()["output"], attempt
        except requests.RequestException as err:
            reason = type(err).__name__
            ms = round((time.perf_counter() - began) * 1000)
            log_event(event="call", run_id=run_id, stage=stage, attempt=attempt, ok=False, error=reason, latency_ms=ms)
            if attempt == config.MAX_RETRIES:
                raise StageError(stage, reason, attempt)
            time.sleep(config.BACKOFF_S * 2 ** attempt)

class State(TypedDict, total=False):
    run_id: str
    topic: str
    facts: str
    draft: str
    verdict: str
    revisions: int
    retries: int
    failed_stage: str
    reason: str

def research_node(state: State):
    try:
        facts, used = call_agent(state["run_id"], "researcher", state["topic"])
    except StageError as err:
        return {"failed_stage": err.stage, "reason": err.reason, "retries": state["retries"] + err.retries}
    return {"facts": facts, "retries": state["retries"] + used}

def write_node(state: State):
    prompt = "FACTS:\n" + state["facts"]
    revising = bool(state["verdict"])
    if revising:
        prompt += f"\n\nPREVIOUS DRAFT:\n{state['draft']}"
        prompt += f"\n\nREVIEWER FEEDBACK:\n{state['verdict']}"
    try:
        draft, used = call_agent(state["run_id"], "writer", prompt)
    except StageError as err:
        return {"failed_stage": err.stage, "reason": err.reason, "retries": state["retries"] + err.retries}
    return {"draft": draft, "retries": state["retries"] + used, "revisions": state["revisions"] + (1 if revising else 0)}

def review_node(state: State):
    try:
        verdict, used = call_agent(state["run_id"], "reviewer", state["draft"])
    except StageError as err:
        return {"failed_stage": err.stage, "reason": err.reason, "retries": state["retries"] + err.retries}
    return {"verdict": verdict, "retries": state["retries"] + used}

def approved(verdict):
    return verdict.strip().upper().startswith("APPROVED")

def after_research(state: State):
    return END if state.get("failed_stage") else "write"

def after_write(state: State):
    return END if state.get("failed_stage") else "review"

def after_review(state: State):
    if state.get("failed_stage") or approved(state["verdict"]):
        return END
    return "write" if state["revisions"] < config.MAX_REVISIONS else END

builder = StateGraph(State)
builder.add_node("research", research_node)
builder.add_node("write", write_node)
builder.add_node("review", review_node)
builder.add_edge(START, "research")
builder.add_conditional_edges("research", after_research)
builder.add_conditional_edges("write", after_write)
builder.add_conditional_edges("review", after_review)
graph = builder.compile()

app = FastAPI(title="Pipeline Orchestrator")

class PipelineRequest(BaseModel):
    topic: str

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "orchestrator",
        "uptime_s": round(time.time() - STARTED),
    }

@app.get("/services")
def services():
    report = {}
    for name, url in URLS.items():
        try:
            info = requests.get(url + "/health", timeout=2).json()
            report[name] = {"up": True, "uptime_s": info["uptime_s"]}
        except requests.RequestException:
            report[name] = {"up": False, "uptime_s": 0}
    return report

@app.post("/pipeline")
def pipeline(req: PipelineRequest):
    run_id = uuid.uuid4().hex[:8]
    began = time.perf_counter()
    state = graph.invoke({
        "run_id": run_id,
        "topic": req.topic,
        "facts": "",
        "draft": "",
        "verdict": "",
        "revisions": 0,
        "retries": 0,
    })
    if state.get("failed_stage"):
        status = "failed"
    elif approved(state["verdict"]):
        status = "approved"
    else:
        status = "rejected"
    result = {
        "run_id": run_id,
        "student": config.STUDENT_SRN,
        "status": status,
        "article": state["draft"],
        "verdict": state["verdict"],
        "revisions": state["revisions"],
        "retries": state["retries"],
        "failed_stage": state.get("failed_stage"),
        "reason": state.get("reason"),
        "latency_ms": round((time.perf_counter() - began) * 1000),
    }
    log_event(event="run", topic=req.topic, **result)
    return result

@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "static" / "index.html")
