# llm.py -- the model for an agent: real (Groq) or a mock
from typing import Any
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
import config

class MockChatModel(BaseChatModel):
    """A fake model, so the pipeline runs without Groq.
    plan(text) -> (tool_name, tool_args), or None for no tool
    finish(text) -> the final reply text"""
    plan: Any = None
    finish: Any = None

    @property
    def _llm_type(self) -> str:
        return "mock"

    def bind_tools(self, tools, **kwargs):
        return self  # the plan function chooses the tool

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        last = messages[-1]
        # A tool has already run: write the final answer from its result
        if isinstance(last, ToolMessage):
            return self._reply(self.finish(last.content))
        user_text = ""
        for m in reversed(messages):
            if isinstance(m, HumanMessage):
                user_text = m.content
                break
        step = self.plan(user_text) if self.plan else None
        if step:
            name, args = step
            call = {"name": name, "args": args, "id": "mock-call-1", "type": "tool_call"}
            return self._reply("", [call])
        return self._reply(self.finish(user_text))

    def _reply(self, text, calls=None):
        message = AIMessage(content=text, tool_calls=calls or [])
        return ChatResult(generations=[ChatGeneration(message=message)])

def get_llm(plan=None, finish=None):
    if config.USE_MOCK_LLM:
        return MockChatModel(plan=plan, finish=finish)
    from langchain_groq import ChatGroq
    return ChatGroq(
        model=config.MODEL_NAME,
        temperature=config.TEMPERATURE,
        api_key=config.GROQ_API_KEY,
    )
