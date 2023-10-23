import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Generator

from openai.openai_object import OpenAIObject

from tinylang.memory import ConversationMemory
from tinylang.memory.base import BaseMemory


class BaseLLM(ABC):
    """
    Abstract Base Class for Large Language Models.
    """

    def __init__(self, memory: BaseMemory | None = None) -> None:
        self.memory = memory or ConversationMemory()

    @abstractmethod
    def load_model(self, model_path: os.PathLike) -> bool:
        """
        Loads the model from the specified path into memory.

        :param model_path: Path to the model.
        """
        raise NotImplementedError

    @abstractmethod
    def chat(self, prompt: str, raw_response: bool = False) -> str | OpenAIObject:
        """
        Simulates a chat interaction with the model.

        :param prompt: The user prompt.
        :param raw_response: Whether to return the raw response or not.
        :return: Generated output text.
        """
        raise NotImplementedError

    @abstractmethod
    def stream_chat(
        self, prompt: str, raw_response: bool = False
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Streams a chat interaction with the model.

        :param prompt: The user prompt.
        :param raw_response: The raw json response.
        :return: Generated output text.
        """
        raise NotImplementedError
