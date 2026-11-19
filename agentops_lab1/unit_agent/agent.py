# agent.py -- the LangGraph agent: a model node and a tools node in a loop
import re
from langchain_core.messages import SystemMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
import config
from llm import get_llm
from tools import convert_units

TOOLS = [convert_units]

def mock_router(text):
    """Mock mode only: pull 'convert 5 km to mile' apart with a regex."""
    pattern = (
        r"convert\s+(-?\d+(?:\.\d+)?)"
        r"\s*([a-zA-Z]+)\s+to\s+([a-zA-Z]+)"
    )
    m = re.search(pattern, text, re.I)
    if m:
        args = {
            "value": float(m.group(1)),
            "from_unit": m.group(2),
            "to_unit": m.group(3),
        }
        return "convert_units", args
    return None

llm = get_llm(mock_router).bind_tools(TOOLS)

def agent_node(state: MessagesState):
    # Put the system prompt (from config) in front of the conversation
    messages = [SystemMessage(content=config.SYSTEM_PROMPT)]
    messages += state["messages"]
    return {"messages": [llm.invoke(messages)]}

builder = StateGraph(MessagesState)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(TOOLS))
builder.add_edge(START, "agent")
# tool requested -> "tools", otherwise END
builder.add_conditional_edges("agent", tools_condition)
# after a tool runs, go back to the model
builder.add_edge("tools", "agent")
graph = builder.compile()
