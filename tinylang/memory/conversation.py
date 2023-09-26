from collections import deque
from dataclasses import dataclass
from typing import Dict, List

from ..messages import AssistantMessage, SystemMessage, UserMessage
from ..messages.base import BaseMessage
from .base import BaseMemory


@dataclass
class ConversationMemory(BaseMemory):
    last_k: int | None

    def __init__(
        self, messages: List[BaseMessage] | None = None, last_k: int | None = None
    ) -> None:
        self._last_k_must_be_positive_and_even(last_k)
        super().__init__(messages)

        self.last_k = last_k or 1
        self._last_k_messages = self.last_k * 2  # keep assistant and user messages

        # use a deque to keep the last k messages
        self.messages = deque(self.messages, maxlen=self._last_k_messages)

    @staticmethod
    def _last_k_must_be_positive_and_even(last_k: int | None) -> int | None:
        if last_k is None:
            return last_k

        if last_k < 1:
            raise ValueError("last_k must be positive")

        # must be even
        if last_k % 2 == 1:
            raise ValueError("last_k must be even")

        return last_k

    def add_message(self, message: BaseMessage) -> None:
        self.messages.append(message)

    def add_user_message(self, message: str) -> None:
        self.add_message(UserMessage(message))

    def add_system_message(self, message: str) -> None:
        self.add_message(SystemMessage(message))

    def add_assistant_message(self, message: str) -> None:
        self.add_message(AssistantMessage(message))

    def to_json(self) -> List[Dict[str, str]]:
        return [message.to_json() for message in self.messages]

    def format_messages(self) -> List[Dict[str, str]]:
        temp = [message.to_json() for message in self.messages]
        return temp[-self._last_k_messages :]
