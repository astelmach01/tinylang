from typing import Dict, Iterator, AsyncIterable, List, Optional
from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion
from .base import ChatBase
from .util import get_api_key
from ..history import ChatHistory


class ChatOpenAI(ChatBase):
    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        init_kwargs: Dict = {},
        system_message: str | None = None,
        chat_history: int = 0,
        previous_history: Optional[List[Dict[str, str]]] = None,
    ) -> None:
        api_key = get_api_key(api_key, "OPENAI_API_KEY")
        init_kwargs.update({"api_key": api_key})
        self.client = OpenAI(**init_kwargs)
        self.async_client = AsyncOpenAI(**init_kwargs)
        self.model = model
        self.system_message = system_message or "You are a helpful assistant."
        self.chat_history = ChatHistory(
            chat_history, self.system_message, previous_history
        )

    def invoke(self, prompt: str) -> str:
        self.chat_history.add_message("user", prompt)
        messages = self.chat_history.get_messages()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False,
        )
        content = response.choices[0].message.content or ""
        self.chat_history.add_message("assistant", content)
        return content

    async def ainvoke(self, prompt: str) -> str:
        self.chat_history.add_message("user", prompt)
        messages = self.chat_history.get_messages()
        response: ChatCompletion = await self.async_client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False,
        )
        content = response.choices[0].message.content or ""
        self.chat_history.add_message("assistant", content)
        return content

    def stream_invoke(self, prompt: str) -> Iterator[str]:
        self.chat_history.add_message("user", prompt)
        messages = self.chat_history.get_messages()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
        )
        full_content = ""
        for chunk in response:
            content = chunk.choices[0].delta.content or ""
            full_content += content
            yield content
        self.chat_history.add_message("assistant", full_content)

    async def astream_invoke(self, prompt: str) -> AsyncIterable[str]:
        self.chat_history.add_message("user", prompt)
        messages = self.chat_history.get_messages()
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
        )
        full_content = ""
        async for chunk in response:
            content = chunk.choices[0].delta.content or ""
            full_content += content
            yield content
        self.chat_history.add_message("assistant", full_content)

    def get_history(self) -> List[Dict[str, str]]:
        return self.chat_history.get_messages()
