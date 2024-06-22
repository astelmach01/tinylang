from typing import Iterator, Dict, AsyncIterable
from abc import ABC, abstractmethod


class ChatBase(ABC):

    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        system_message: str | None = None,
        init_kwargs: Dict = {},
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def invoke(self, user_input: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def ainvoke(self, user_input: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def stream_invoke(self, user_input: str) -> Iterator[str]:
        raise NotImplementedError

    @abstractmethod
    async def astream_invoke(self, user_input: str) -> AsyncIterable[str]:
        raise NotImplementedError
