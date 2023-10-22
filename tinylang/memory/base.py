"""Base class for memory."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, MutableSequence

from ..messages.base import BaseMessage


@dataclass  # type: ignore
class BaseMemory(ABC):
    def __init__(self, messages: MutableSequence[BaseMessage] | None = None) -> None:
        self.messages = messages or []

    @abstractmethod
    def add_message(self, message: BaseMessage) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_user_message(self, message: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_system_message(self, message: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_assistant_message(self, message: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def to_json(self) -> List[Dict]:
        raise NotImplementedError

    def format_messages(self, include_image: bool = True) -> List[Dict]:
        return [message.to_json(include_image) for message in self.messages]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.messages})"

    def __str__(self) -> str:
        return str(self.messages)
