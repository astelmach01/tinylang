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
        self.messages: List[Dict[str, str]] = []
        if previous_history:
            for message in previous_history:
                if message["role"] != "system":
                    self.add_message(message["role"], message["content"])

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})

        # TODO - change this to user-assistant roles and not the entire list
        if self.max_history > 0:
            # Keep only the last max_history * 2 messages
            self.messages = self.messages[-(self.max_history * 2) :]

    def get_messages(self) -> List[Dict[str, str]]:
        return [{"role": "system", "content": self.system_message}] + self.messages

    def clear(self) -> None:
        self.messages.clear()
