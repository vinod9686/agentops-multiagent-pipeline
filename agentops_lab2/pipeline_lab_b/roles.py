# roles.py -- what makes the three agents different from each other
import re
from langchain_core.tools import tool

MIN_WORDS = 30  # the reviewer approves drafts of at least this length

KB = {
    "docker": [
        "Docker packages an application with everything it needs to run.",
        "A container starts in seconds because it shares the host kernel.",
        "An image is a read-only template; a container is a running copy.",
        "Docker Compose starts several containers together from one file.",
    ],
    "langgraph": [
        "LangGraph models an agent as a graph of nodes and edges.",
        "A node is a Python function that reads and updates shared state.",
        "Conditional edges let the graph choose the next node at run time.",
        "The same graph can loop, for example agent to tools and back.",
    ],
    "fastapi": [
        "FastAPI turns ordinary Python functions into web endpoints.",
        "Pydantic models check that incoming JSON has the right shape.",
        "It generates interactive API documentation automatically.",
        "Uvicorn is the server that actually runs a FastAPI application.",
    ],
    "agentops": [
        "AgentOps means running AI agents reliably in production.",
        "It covers deployment, monitoring, logging, retries and costs.",
        "Success rate and latency show how healthy an agent is.",
        "Failures are expected, so every call needs a timeout and retries.",
    ],
    "latency": [
        "Latency measures the delay experienced during end to end request processing.",
        "High response latency negatively degrades user experience in interactive systems.",
        "Network latency between microservices can accumulate across multi agent workflows.",
        "Optimizing agent inference and caching dramatically reduces overall pipeline latency.",
    ],
}

@tool
def lookup_facts(topic: str) -> str:
    """Return known facts about a topic from the local knowledge base."""
    facts = KB.get(topic.strip().lower())
    if not facts:
        return f"No facts found for '{topic}'."
    return "\n".join("- " + fact for fact in facts)

@tool
def count_words(text: str) -> str:
    """Count the words in a text."""
    return f"Word count: {len(text.split())}"

def writer_mock(text):
    """Mock writer: join the facts into a paragraph."""
    if "REVIEWER FEEDBACK" in text:  # a revision round
        draft = text.split("PREVIOUS DRAFT:")[1]
        draft = draft.split("REVIEWER FEEDBACK:")[0].strip()
        extra = " In short, this makes systems easier to run and debug."
        return draft + extra
    facts = [ln[2:] for ln in text.splitlines() if ln.startswith("- ")]
    if not facts:
        return "No facts were available, so there is little to say here."
    return "Here is a short note. " + " ".join(facts)

def reviewer_mock(tool_result):
    """Mock reviewer: approve if the draft is long enough."""
    words = int(re.search(r"\d+", tool_result).group())
    if words >= MIN_WORDS:
        return "APPROVED: the draft is long enough and clear."
    return f"REVISE: only {words} words, add more detail."

ROLES = {
    "researcher": {
        "prompt": (
            "You are a researcher. Call the lookup_facts tool with the "
            "topic you are given, then reply with the facts it returns."
        ),
        "tools": [lookup_facts],
        "plan": lambda text: ("lookup_facts", {"topic": text}),
        "finish": lambda tool_result: tool_result,
    },
    "writer": {
        "prompt": (
            "You are a writer. Write one short paragraph of 40 to 80 "
            "words using ONLY the facts you are given. If the facts say "
            "No facts found, reply only: No facts are available. "
            "Never add anything that is not in the facts, even if "
            "there is REVIEWER FEEDBACK. If there is feedback, rewrite "
            "the previous draft to fix it."
        ),
        "tools": [],
        "plan": None,
        "finish": writer_mock,
    },
    "reviewer": {
        "prompt": (
            "You are a reviewer. Call count_words with the draft. Reply "
            "with ONE line that starts with APPROVED: or REVISE: and "
            f"gives a short reason. Approve only if it has {MIN_WORDS} "
            "or more words and is clear."
        ),
        "tools": [count_words],
        "plan": lambda text: ("count_words", {"text": text}),
        "finish": reviewer_mock,
    },
}
