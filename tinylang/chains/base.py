from openai.openai_object import OpenAIObject

from tinylang.llms.base import BaseLLM
from tinylang.memory import ConversationMemory
from tinylang.memory.base import BaseMemory
from tinylang.messages import SystemMessage


class Chain:
    def __init__(
        self,
        llm: BaseLLM,
        memory: BaseMemory | None = None,
        prompt: str | SystemMessage | None = None,
    ) -> None:
        self.llm = llm
        self.memory = memory or ConversationMemory()
        self.llm.memory = self.memory

        if isinstance(prompt, SystemMessage):
            self.memory.add_message(prompt)

        elif isinstance(prompt, str):
            self.memory.add_system_message(prompt)

    def run(self, prompt: str, raw_response: bool = False) -> str | OpenAIObject:
        return self.llm.chat(prompt, raw_response)
