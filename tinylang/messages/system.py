from typing import Dict

from .base import BaseMessage


class SystemMessage(BaseMessage):
    def __init__(self, content: str, prefix: str = "system") -> None:
        super().__init__(content, prefix)

    @staticmethod
    def from_json(json: Dict[str, str]) -> "SystemMessage":
        return SystemMessage(content=json["content"], prefix=json["prefix"])
