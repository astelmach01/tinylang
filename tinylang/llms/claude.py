from typing import Dict, Iterator, AsyncIterable, List, Optional
from .base import ChatBase
import anthropic
from anthropic import AsyncAnthropic
from .util import get_api_key
from ..history import ChatHistory


class ChatClaude(ChatBase):
    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        init_kwargs: Dict = {},
        system_message: str | None = None,
        chat_history: int = 0,
        previous_history: Optional[List[Dict[str, str]]] = None,
    ) -> None:
        api_key = get_api_key(api_key, "ANTHROPIC_API_KEY")
        init_kwargs.update({"api_key": api_key})
        self.client = anthropic.Anthropic(**init_kwargs)
        self.async_client = AsyncAnthropic(**init_kwargs)
        self.model = model
        self.system_message = system_message or "You are a helpful assistant."
        self.chat_history = ChatHistory(
            chat_history, self.system_message, previous_history
        )

    def invoke(self, prompt: str, max_tokens: int = 2048) -> str:
        self.chat_history.add_message("user", prompt)
        messages = self.chat_history.get_messages()[1:]  # Exclude system message
        response = self.client.messages.create(
            model=self.model,
            system=self.system_message,
            max_tokens=max_tokens,
            messages=messages,
        )
        content = response.content[0].text or ""
        self.chat_history.add_message("assistant", content)
        return content

    async def ainvoke(self, prompt: str) -> str:
        self.chat_history.add_message("user", prompt)
        messages = self.chat_history.get_messages()[1:]  # Exclude system message
        response = await self.async_client.messages.create(
            model=self.model,
            system=self.system_message,
            max_tokens=2048,
            messages=messages,
        )
        content = response.content[0].text or ""
        self.chat_history.add_message("assistant", content)
        return content

    def stream_invoke(self, prompt: str) -> Iterator[str]:
        self.chat_history.add_message("user", prompt)
        messages = self.chat_history.get_messages()[1:]  # Exclude system message
        with self.client.messages.stream(
            model=self.model,
            system=self.system_message,
            max_tokens=2048,
            messages=messages,
        ) as stream:
            full_content = ""
            for text in stream.text_stream:
                full_content += text
                yield text
        self.chat_history.add_message("assistant", full_content)

    async def astream_invoke(self, prompt: str) -> AsyncIterable[str]:
        self.chat_history.add_message("user", prompt)
        messages = self.chat_history.get_messages()[1:]  # Exclude system message
        async with self.async_client.messages.stream(
            model=self.model,
            system=self.system_message,
            max_tokens=2048,
            messages=messages,
        ) as stream:
            full_content = ""
            async for text in stream.text_stream:
                full_content += text
                yield text
        self.chat_history.add_message("assistant", full_content)
