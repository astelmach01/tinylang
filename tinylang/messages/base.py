from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Literal

from .utils import from_json

RoleType = Literal["system", "user", "assistant"]


@dataclass  # type: ignore
class BaseMessage(ABC):
    role: RoleType
    content: str

    def __init__(self, content: str, role: RoleType) -> None:
        self.content = content
        self.role = role

    def to_json(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}

    def copy(self) -> "BaseMessage":
        return self.from_json(self.to_json())

    @staticmethod
    @abstractmethod
    def from_json(json: Dict[str, str]) -> "BaseMessage":
        return from_json(json)  # type: ignore

    def __str__(self) -> str:
        return f"{self.role}: {self.content}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.role}, {self.content})"
