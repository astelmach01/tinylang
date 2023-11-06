import os
from typing import Any, Dict, Generator

from openai import OpenAI as OpenAIClient

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
        self.kwargs = (
            kwargs  # kwargs passed into the openai.ChatCompletion.create() method
        )

        self.client = OpenAIClient(
            api_key=self.openai_api_key, organization=self.openai_organization
        )

    def load_model(self, model_path: os.PathLike) -> bool:
        """
        Loads a local model from a path.
        """
        return True  # since we're using the API

    def chat(
        self,
        prompt: str,
        raw_response: bool = False,
        image: Image | None = None,
        **kwargs: Dict,
    ) -> str:
        # TODO: move this elsewhere
        # be consistent with the prefix
        prefix = "user"
        for message in self.memory.messages:
            if isinstance(message, UserMessage):
                prefix = message.prefix
                break

        self.memory.add_user_message(message=prompt, prefix=prefix, image=image)

        completion_kwargs = self.kwargs.copy()
        completion_kwargs.update(kwargs)

        api_response = self.client.chat.completions.create(
            model=self.model,
            messages=self.memory.format_messages(),
            **completion_kwargs,
        )  # type: ignore

        chat_response: str = api_response.model_dump()["choices"][0]["message"][
            "content"
        ]
        self.memory.add_assistant_message(chat_response)

        if raw_response:
            return api_response  # type: ignore

        return chat_response

    def stream_chat(
        self, prompt: str, raw_response: bool = False, **kwargs: Dict
    ) -> Generator[Dict[str, Any], None, None]:
        self.memory.add_user_message(prompt)

        completion_kwargs = self.kwargs.copy()
        completion_kwargs.update(kwargs)

        api_response = self.client.chat.completions.create(
            model=self.model,
            messages=self.memory.format_messages(),
            stream=True,
            **completion_kwargs,
        )  # type: ignore

        aggregated_content = ""
        for chunk in api_response:
            content = chunk.choices[0].delta.content or ""

            # if there's no content
            if not content:
                continue

            aggregated_content += content

            yield chunk if raw_response else content

        self.memory.add_assistant_message(aggregated_content)
