from typing import Dict

from .base import BaseMessage


class AssistantMessage(BaseMessage):
    def __init__(self, content: str, prefix: str = "assistant") -> None:
        super().__init__(content, prefix)

    @staticmethod
    def from_json(json: Dict[str, str]) -> "AssistantMessage":
        return AssistantMessage(content=json["content"], prefix=json["prefix"])
