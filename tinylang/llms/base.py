from typing import Iterator, Dict, AsyncIterable, List, Any, Optional
from abc import ABC, abstractmethod


class ChatBase(ABC):
    @abstractmethod
    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        system_message: str | None = None,
        init_kwargs: Dict = {},
        chat_history: int = 0,
        previous_history: Optional[List[Dict[str, str]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[str] = "auto",
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def invoke(self, user_input: str) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def ainvoke(self, user_input: str) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def stream_invoke(self, user_input: str) -> Iterator[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def astream_invoke(self, user_input: str) -> AsyncIterable[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_history(self) -> List[Dict[str, str]]:
        raise NotImplementedError

    @abstractmethod
    def clear_history(self) -> None:
        raise NotImplementedError
