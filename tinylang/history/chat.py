from collections import deque
from typing import List, Dict, Optional


class ChatHistory:
    def __init__(
        self,
        max_history: int,
        system_message: str,
        previous_history: Optional[List[Dict[str, str]]] = None,
    ):
        self.max_history = max_history
        self.system_message = system_message
        self.messages: deque = deque(
            maxlen=max_history * 2
        )  # *2 to account for both user and assistant messages

        if previous_history:
            for message in previous_history:
                if message["role"] != "system":
                    self.add_message(message["role"], message["content"])

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})

    def get_messages(self) -> List[Dict[str, str]]:
        return [{"role": "system", "content": self.system_message}] + list(
            self.messages
        )

    def clear(self) -> None:
        self.messages.clear()
