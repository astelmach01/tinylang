from typing import Dict

from .base import BaseMessage


class AssistantMessage(BaseMessage):
    def __init__(self, content: str) -> None:
        super().__init__(content, "assistant")

    @staticmethod
    def from_json(json: Dict[str, str]) -> "AssistantMessage":
        return AssistantMessage(content=json["content"])
