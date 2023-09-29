from abc import ABC, abstractmethod
from typing import Any, Dict, Generator, Union

from tinylang.memory import ConversationMemory
from tinylang.memory.base import BaseMemory


class BaseLLM(ABC):
    """
    Abstract Base Class for Large Language Models.
    """

    def __init__(self, memory: BaseMemory | None = None) -> None:
        self.memory = memory or ConversationMemory()

    @abstractmethod
    def load_model(self, model_path: str) -> bool:
        """
        Loads the model from the specified path into memory.

        :param model_path: Path to the model.
        """
        raise NotImplementedError

    @abstractmethod
    def chat(
        self, prompt: str, stream: bool = False, raw_response: bool = False
    ) -> Union[str, Generator[Dict[str, Any], None, None]]:
        """
        Simulates a chat interaction with the model.

        :param prompt: The user prompt.
        :param stream: Whether to stream the response or not.
        :param raw_response: Whether to return the raw response or not.
        :return: Generated output text.
        """
        raise NotImplementedError
