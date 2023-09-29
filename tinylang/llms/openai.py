from typing import Any, Dict, Generator, Union

import openai
from openai.openai_object import OpenAIObject

from tinylang.llms.base import BaseLLM
from tinylang.memory.base import BaseMemory


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

    def load_model(self, model_path: str) -> bool:
        return True  # nothing to do here since using APImake

    def _stream_response(
        self, api_response: OpenAIObject, raw_response: bool
    ) -> Generator[Dict[str, Any], None, None]:
        aggregated_content = ""
        for chunk in api_response:
            content = chunk["choices"][0]["delta"].get("content")

            # if there's no content
            if not content:
                continue

            aggregated_content += content

            yield chunk if raw_response else content

        self.memory.add_assistant_message(aggregated_content)

    def chat(
        self, prompt: str, stream: bool = False, raw_response: bool = False
    ) -> Union[str, Generator[Dict[str, Any], None, None]]:
        self.memory.add_user_message(prompt)

        api_response: OpenAIObject = openai.ChatCompletion.create(
            model=self.model,
            messages=self.memory.format_messages(),
            stream=stream,
            **self.kwargs,
        )

        if stream:
            return self._stream_response(api_response, raw_response)
        else:
            chat_response: str = api_response["choices"][0]["message"]["content"]
            self.memory.add_assistant_message(chat_response)
            return chat_response
