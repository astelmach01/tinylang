from typing import Dict, Iterator, AsyncIterable, List, Optional
from .util import get_api_key
from .base import ChatBase
from ..history import ChatHistory
import google.generativeai as genai


class ChatGemini(ChatBase):
    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        system_message: str | None = None,
        chat_history: int = 0,
        previous_history: Optional[List[Dict[str, str]]] = None,
        init_kwargs: Dict = {},
    ) -> None:
        self.model = model
        self.api_key = api_key
        self.system_message = system_message or "You are a helpful assistant."
        self.init_kwargs = init_kwargs
        self.chat_history = ChatHistory(
            chat_history, self.system_message, previous_history
        )

        api_key = get_api_key(api_key, "GOOGLE_API_KEY")
        genai.configure(api_key=api_key)

        self.client = genai.GenerativeModel(model, **init_kwargs)
        self.chat_session = self.client.start_chat(
            history=self._convert_history_to_gemini_format()
        )

    def _convert_history_to_gemini_format(self) -> List[Dict[str, str]]:
        gemini_history = []
        for message in self.chat_history.get_messages():
            role = (
                "model"
                if message["role"] == "assistant" or message["role"] == "system"
                else message["role"]
            )
            gemini_history.append({"role": role, "parts": [message["content"]]})
        return gemini_history

    def _update_chat_history(self, role: str, content: str):
        self.chat_history.add_message(role, content)

    def invoke(self, prompt: str) -> str:
        response = self.chat_session.send_message(prompt)
        self.chat_history.add_message("user", prompt)
        content = response.text or ""
        self._update_chat_history("model", content)
        return content

    async def ainvoke(self, prompt: str) -> str:
        response = await self.chat_session.send_message_async(prompt)
        self.chat_history.add_message("user", prompt)
        content = response.text or ""
        self._update_chat_history("model", content)
        return content

    def stream_invoke(self, prompt: str) -> Iterator[str]:
        response = self.chat_session.send_message(prompt, stream=True)
        self.chat_history.add_message("user", prompt)
        full_response = ""
        for chunk in response:
            content = chunk.text or ""
            full_response += content
            yield content
        self._update_chat_history("model", full_response)

    async def astream_invoke(self, prompt: str) -> AsyncIterable[str]:
        response = await self.chat_session.send_message_async(prompt, stream=True)
        self.chat_history.add_message("user", prompt)
        full_response = ""
        async for chunk in response:
            content = chunk.text or ""
            full_response += content
            yield content
        self._update_chat_history("model", full_response)

    def get_history(self) -> List[Dict[str, str]]:
        return self.chat_history.get_messages()
