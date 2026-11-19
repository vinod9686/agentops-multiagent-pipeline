# llm.py -- gives the agent a language model: real (Groq) or a mock
from typing import Any
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
import config

class MockChatModel(BaseChatModel):
    """A fake model for when Groq is unavailable.
    It follows the same tool-calling loop as the real one."""
    # function: user text -> (tool_name, tool_args), or None
    router: Any = None

    @property
    def _llm_type(self) -> str:
        return "mock"

    def bind_tools(self, tools, **kwargs):
        return self  # nothing to bind: the router picks the tool

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        last = messages[-1]
        # Second pass: a tool has already run, so write the final answer
        if isinstance(last, ToolMessage):
            message = AIMessage(content=f"(mock) {last.content}")
            return self._result(message)
        # First pass: decide whether to call a tool
        user_text = ""
        for m in reversed(messages):
            if isinstance(m, HumanMessage):
                user_text = m.content
                break
        plan = self.router(user_text) if self.router else None
        if plan:
            name, args = plan
            call = {"name": name, "args": args, "id": "mock-call-1", "type": "tool_call"}
            message = AIMessage(content="", tool_calls=[call])
        else:
            message = AIMessage(content="(mock) No tool matched.")
        return self._result(message)

    def _result(self, message):
        return ChatResult(generations=[ChatGeneration(message=message)])

def get_llm(mock_router=None):
    if config.USE_MOCK_LLM:
        return MockChatModel(router=mock_router)
    from langchain_groq import ChatGroq
    return ChatGroq(
        model=config.MODEL_NAME,
        temperature=config.TEMPERATURE,
        api_key=config.GROQ_API_KEY,
    )
