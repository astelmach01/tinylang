from typing import Dict, Iterator, AsyncIterable
from .base import ChatBase
import anthropic
from anthropic import AsyncAnthropic
from .util import get_api_key


class ChatClaude(ChatBase):
    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        init_kwargs: Dict = {},
        system_message: str | None = None,
    ) -> None:
        api_key = get_api_key(api_key, "ANTHROPIC_API_KEY")
        init_kwargs.update({"api_key": api_key})

        self.client = anthropic.Anthropic(**init_kwargs)
        self.async_client = AsyncAnthropic(**init_kwargs)

        self.model = model
        self.system_message = system_message or "You are a helpful assistant."

    def invoke(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            system=self.system_message,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        return response.content[0].text or ""

    async def ainvoke(self, prompt: str) -> str:
        response = await self.async_client.messages.create(
            model=self.model,
            system=self.system_message,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        return response.content[0].text or ""

    def stream_invoke(self, prompt: str) -> Iterator[str]:
        with self.client.messages.stream(
            model=self.model,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        ) as stream:
            for text in stream.text_stream:
                yield text

        final_message = stream.get_final_message()
        final_message = final_message.content[0].text or ""

    async def astream_invoke(self, prompt: str) -> AsyncIterable[str]:
        async with self.async_client.messages.stream(
            model=self.model,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        ) as stream:
            async for text in stream.text_stream:
                yield text

        final_message = await stream.get_final_message()
        final_message = final_message.content[0].text or ""
