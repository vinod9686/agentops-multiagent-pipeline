# agent_main.py -- one agent service; ROLE decides which agent it is
import random
import time
from fastapi import FastAPI, HTTPException
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel
import config
from llm import get_llm
from roles import ROLES

if config.ROLE not in ROLES:
    raise SystemExit(f"Unknown ROLE {config.ROLE!r}. Use: {list(ROLES)}")

role = ROLES[config.ROLE]
TOOLS = role["tools"]
llm = get_llm(role["plan"], role["finish"])
if TOOLS:
    llm = llm.bind_tools(TOOLS)

def agent_node(state: MessagesState):
    messages = [SystemMessage(content=role["prompt"])]
    messages += state["messages"]
    return {"messages": [llm.invoke(messages)]}

builder = StateGraph(MessagesState)
builder.add_node("agent", agent_node)
builder.add_edge(START, "agent")
if TOOLS:  # agent -> tools -> agent loop, as in Lab 1
    builder.add_node("tools", ToolNode(TOOLS))
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")
else:  # no tools: one model call and done
    builder.add_edge("agent", END)
graph = builder.compile()

app = FastAPI(title=f"{config.ROLE} agent")
STARTED = time.time()

class RunRequest(BaseModel):
    text: str

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": config.ROLE,
        "mock_llm": config.USE_MOCK_LLM,
        "uptime_s": round(time.time() - STARTED),
    }

@app.post("/run")
def run(req: RunRequest):
    start = time.perf_counter()
    if config.DELAY_MS:  # injected slowness
        time.sleep(config.DELAY_MS / 1000)
    if random.random() < config.FAIL_RATE:  # injected failure
        raise HTTPException(status_code=503, detail="Injected failure")
    try:
        inputs = {"messages": [HumanMessage(content=req.text)]}
        result = graph.invoke(inputs)
    except Exception as err:  # bad key, no internet, rate limit...
        raise HTTPException(status_code=502, detail=f"Agent failed: {err}")
    return {
        "role": config.ROLE,
        "output": result["messages"][-1].content,
        "latency_ms": round((time.perf_counter() - start) * 1000),
    }
