from typing import Dict, Iterator, AsyncIterable
from .util import get_api_key
import google.generativeai as genai


class ChatGemini:
    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        init_kwargs: Dict = {},
        system_message: str | None = None,
    ) -> None:
        api_key = get_api_key(api_key, "GOOGLE_API_KEY")
        genai.configure(api_key=api_key)

        self.system_message = system_message or "You are a helpful assistant."
        self.client = genai.GenerativeModel(
            model, system_instruction=system_message, **init_kwargs
        )

    def invoke(self, prompt: str) -> str:
        response = self.client.generate_content(prompt)
        return response.text

    async def ainvoke(self, prompt: str) -> str:
        response = await self.client.generate_content_async(prompt)
        return response.text

    def stream_invoke(self, prompt: str) -> Iterator[str]:
        response = self.client.generate_content(prompt, stream=True)
        for chunk in response:
            yield chunk.text

    async def astream_invoke(self, prompt: str) -> AsyncIterable[str]:
        response = await self.client.generate_content_async(prompt, stream=True)
        async for chunk in response:
            yield chunk.text
