from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict

from tinylang.images import Image
from .utils import from_json


@dataclass  # type: ignore
class BaseMessage(ABC):
    prefix: str
    content: str
    image: Image | None

    def __init__(self, content: str, prefix: str, image: Image | None = None) -> None:
        self.content = content
        self.prefix = prefix
        self.image = image

    def to_json(self, style: str = "openai") -> Dict:
        result = {"role": self.prefix, "content": self.content}

        if style == "openai" and self.image is not None:
            result["image"] = self.image.to_numpy()  # type: ignore

        elif style == "copy" and self.image is not None:
            result["image"] = self.image.to_numpy()  # type: ignore
        return result

    @staticmethod
    @abstractmethod
    def from_json(json: Dict) -> "BaseMessage":
        return from_json(json)  # type: ignore

    def copy(self) -> "BaseMessage":
        return self.from_json(self.to_json(style="copy"))

    def __str__(self) -> str:
        return f"{self.prefix}: {self.content}"

    def __repr__(self) -> str:
        result = f"{self.__class__.__name__}({self.prefix}, {self.content}"
        if self.image is not None:
            result += f", {self.image}"

        result += ")"
        return result
