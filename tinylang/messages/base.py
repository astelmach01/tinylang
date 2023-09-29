from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict

from .utils import from_json


@dataclass  # type: ignore
class BaseMessage(ABC):
    prefix: str
    content: str

    def __init__(self, content: str, prefix: str) -> None:
        self.content = content
        self.prefix = prefix

    def to_json(self) -> Dict[str, str]:
        return {"role": self.prefix, "content": self.content}

    def copy(self) -> "BaseMessage":
        return self.from_json(self.to_json())

    @staticmethod
    @abstractmethod
    def from_json(json: Dict[str, str]) -> "BaseMessage":
        return from_json(json)  # type: ignore

    def __str__(self) -> str:
        return f"{self.prefix}: {self.content}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.prefix}, {self.content})"
