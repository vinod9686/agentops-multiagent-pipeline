# agent.py -- same graph as Experiment 1A; supports text analysis and longest word
from langchain_core.messages import SystemMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
import config
from llm import get_llm
from tools import analyze_text, find_longest_word

TOOLS = [analyze_text, find_longest_word]

def mock_router(text):
    """Mock mode only: routes to find_longest_word if 'longest' is present, else analyze_text."""
    if "longest" in text.lower():
        return "find_longest_word", {"text": text}
    return "analyze_text", {"text": text}

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
