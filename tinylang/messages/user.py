from typing import Dict

from tinylang.messages.base import BaseMessage


class UserMessage(BaseMessage):
    def __init__(self, content: str) -> None:
        super().__init__(content=content, role="user")

    @staticmethod
    def from_json(json: Dict[str, str]) -> "UserMessage":
        return UserMessage(content=json["content"])
