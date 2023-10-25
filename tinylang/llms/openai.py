import os
from typing import Any, Dict, Generator, MutableSequence

import openai
from openai.openai_object import OpenAIObject

from tinylang.images import Image
from tinylang.llms.base import BaseLLM
from tinylang.memory.base import BaseMemory
from tinylang.messages import UserMessage, BaseMessage


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
        self.kwargs = (
            kwargs  # kwargs passed into the openai.ChatCompletion.create() method
        )

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
        # TODO: move this elsewhere
        # be consistent with the prefix
        def get_prefix(messages: MutableSequence[BaseMessage]) -> str:
            return next(
                (
                    message.prefix
                    for message in messages
                    if isinstance(message, UserMessage)
                ),
                "user",
            )

        self.memory.add_user_message(
            message=prompt, prefix=get_prefix(self.memory.messages), image=image
        )

        api_response: OpenAIObject = openai.ChatCompletion.create(
            model=self.model,
            messages=self.memory.format_messages(style="openai"),
            image=image.to_numpy() if image is not None else None,
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
