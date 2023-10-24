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
        return UserMessage(
            content=json["content"],
            image=json.get("image"),  # type: ignore
            prefix=json.get("role", "user"),
        )
