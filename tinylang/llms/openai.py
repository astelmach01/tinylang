from typing import Dict, Iterator, AsyncIterable
import os
from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion
from .base import ChatBase
from .util import get_api_key


class ChatOpenAI(ChatBase):
    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        init_kwargs: Dict = {},
        system_message: str | None = None,
    ) -> None:

        api_key = get_api_key(api_key, "OPENAI_API_KEY")
        init_kwargs.update({"api_key": api_key})

        self.client = OpenAI(**init_kwargs)
        self.async_client = AsyncOpenAI(**init_kwargs)

        self.model = model
        self.system_message = system_message or "You are a helpful assistant."

    def invoke(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": prompt},
            ],
            stream=False,
        )
        return response.choices[0].message.content or ""

    async def ainvoke(self, prompt: str) -> str:
        response: ChatCompletion = await self.async_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": prompt},
            ],
            stream=False,
        )
        return response.choices[0].message.content or ""

    def stream_invoke(self, prompt: str) -> Iterator[str]:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )

        message = ""
        for chunk in response:
            content = chunk.choices[0].delta.content or ""
            message += content
            yield content

    async def astream_invoke(self, prompt: str) -> AsyncIterable[str]:
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )
        message = ""
        async for chunk in response:
            content = chunk.choices[0].delta.content or ""
            message += content
            yield content
