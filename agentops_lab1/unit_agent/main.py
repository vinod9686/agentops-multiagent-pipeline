# main.py -- hosts the agent as a REST web service
import time
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from langchain_core.messages import HumanMessage, ToolMessage
from pydantic import BaseModel
import config
from agent import graph

app = FastAPI(title="Unit Converter Agent")

class RunRequest(BaseModel):
    task: str  # the JSON body must look like {"task": "..."}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": config.MODEL_NAME,
        "mock_llm": config.USE_MOCK_LLM,
    }

@app.post("/run")
def run(req: RunRequest):
    start = time.perf_counter()
    inputs = {"messages": [HumanMessage(content=req.task)]}
    try:
        result = graph.invoke(inputs)
    except Exception as err:  # wrong key, no internet, rate limit...
        raise HTTPException(status_code=502, detail=f"Agent failed: {err}")
    messages = result["messages"]
    tools_used = [m.name for m in messages if isinstance(m, ToolMessage)]
    return {
        "answer": messages[-1].content,
        "tools_used": tools_used,
        "model": config.MODEL_NAME,
        "latency_ms": round((time.perf_counter() - start) * 1000),
    }

@app.get("/")
def index():
    page = Path(__file__).parent / "static" / "index.html"
    return FileResponse(page)
