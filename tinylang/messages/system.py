from typing import Dict

from .base import BaseMessage


class SystemMessage(BaseMessage):
    def __init__(self, content: str) -> None:
        super().__init__(content, "system")

    @staticmethod
    def from_json(json: Dict[str, str]) -> "SystemMessage":
        return SystemMessage(content=json["content"])
