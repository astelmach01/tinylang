from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict

import numpy as np

from .utils import from_json


@dataclass  # type: ignore
class BaseMessage(ABC):
    prefix: str
    content: str
    image: np.ndarray | None

    def __init__(
        self, content: str, prefix: str, image: np.ndarray | None = None
    ) -> None:
        self.content = content
        self.prefix = prefix
        self.image = image

    def to_json(self, include_image: bool = True) -> Dict:
        result = {"role": "user", "prefix": self.prefix, "content": self.content}

        if include_image and self.image is not None:
            result["image"] = self.image  # type: ignore
        return result

    @staticmethod
    @abstractmethod
    def from_json(json: Dict) -> "BaseMessage":
        return from_json(json)  # type: ignore

    def copy(self) -> "BaseMessage":
        return self.from_json(self.to_json(include_image=True))

    def __str__(self) -> str:
        return f"{self.prefix}: {self.content}"

    def __repr__(self) -> str:
        result = f"{self.__class__.__name__}({self.prefix}, {self.content}"
        if self.image is not None:
            result += f", {self.image}"

        result += ")"
        return result
