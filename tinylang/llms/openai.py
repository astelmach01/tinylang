import os
from typing import Any, Dict, Generator

import openai
from openai.openai_object import OpenAIObject

from tinylang.images import Image
from tinylang.llms.base import BaseLLM
from tinylang.memory.base import BaseMemory
from tinylang.messages import UserMessage


class OpenAI(BaseLLM):
    def __init__(
        self,
        openai_api_key: str,
        openai_organization: str,
        model: str,
        memory: BaseMemory | None = None,
        **kwargs: Dict,
    ) -> None:
        super().__init__(memory)
        self.openai_api_key = openai_api_key
        self.openai_organization = openai_organization
        self.model = model
        self.kwargs = kwargs

        openai.api_key = self.openai_api_key
        openai.organization = self.openai_organization

    def load_model(self, model_path: os.PathLike) -> bool:
        """
        Loads a local model from a path.
        """
        return True  # since we're using the API

    def chat(
        self, prompt: str, raw_response: bool = False, image: Image | None = None
    ) -> str | OpenAIObject:
        np_image = image.to_numpy() if image else None
        message = UserMessage(prompt, image=np_image)
        self.memory.add_message(message)

        api_response: OpenAIObject = openai.ChatCompletion.create(
            model=self.model,
            messages=self.memory.format_messages(include_image=False),
            **self.kwargs,
        )

        chat_response: str = api_response["choices"][0]["message"]["content"]
        self.memory.add_assistant_message(chat_response)

        if raw_response:
            return api_response

        return chat_response

    def stream_chat(
        self, prompt: str, raw_response: bool = False
    ) -> Generator[Dict[str, Any], None, None]:
        self.memory.add_user_message(prompt)

        api_response: OpenAIObject = openai.ChatCompletion.create(
            model=self.model,
            messages=self.memory.format_messages(),
            stream=True,
            **self.kwargs,
        )

        aggregated_content = ""
        for chunk in api_response:
            content = chunk["choices"][0]["delta"].get("content")

            # if there's no content
            if not content:
                continue

            aggregated_content += content

            yield chunk if raw_response else content

        self.memory.add_assistant_message(aggregated_content)
