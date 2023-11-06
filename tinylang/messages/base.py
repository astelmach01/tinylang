import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict

from tinylang.images import Image
from .utils import from_json


@dataclass  # type: ignore
class BaseMessage(ABC):
    prefix: str
    text: str
    image: Image | None
    image_dir: os.PathLike

    def __init__(
        self,
        text: str,
        prefix: str,
        image: Image | None = None,
    ) -> None:
        self.prefix = prefix
        self.text = text
        self.image = image

    def to_json(self) -> Dict:
        result = {"role": self.prefix}

        content = [{"type": "text", "text": self.text}]

        if self.image is not None:
            content.append({"type": "image_url", "image_url": self.image.to_url()})

        result["content"] = content

        return result

    @staticmethod
    @abstractmethod
    def from_json(json: Dict) -> "BaseMessage":
        return from_json(json)  # type: ignore

    def copy(self) -> "BaseMessage":
        return self.from_json(self.to_json())

    def __str__(self) -> str:
        return str(self.to_json())

    def __repr__(self) -> str:
        return str(self.to_json())
