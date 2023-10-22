from typing import Dict

import numpy as np

from tinylang.messages.base import BaseMessage


class UserMessage(BaseMessage):
    def __init__(
        self, content: str, prefix: str = "user", image: np.ndarray | None = None
    ) -> None:
        super().__init__(content, prefix, image)

    @staticmethod
    def from_json(json: Dict[str, str]) -> "UserMessage":
        if "image" in json:
            return UserMessage(
                content=json["content"],
                image=np.array(json["image"]),
                prefix=json["prefix"],
            )
        return UserMessage(content=json["content"], prefix=json["prefix"])
