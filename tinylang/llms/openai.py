from typing import Dict, List, Any, Optional, Iterator, AsyncIterable, AsyncIterator
import json
from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion
from .base import ChatBase
from .util import get_api_key
from ..history import ChatHistory
from ..tools.tool import Tool, process_tools


class ChatOpenAI(ChatBase):
    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        init_kwargs: Dict = {},
        system_message: str | None = None,
        chat_history: int = 0,
        previous_history: Optional[List[Dict[str, str]]] = None,
        tools: Optional[List[Tool]] = None,
        tool_choice: Optional[str] = None,
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
        self.original_tools = tools
        self.processed_tools = process_tools(tools) if tools else None
        self.tool_choice = tool_choice if tools else None

    def get_tool_function(self, function_name: str):
        if not self.original_tools:
            raise ValueError("No tools have been set for this chat instance")
        for tool in self.original_tools:
            if tool.name == function_name:
                return tool.function
        raise ValueError(f"Function {function_name} not found in tools")

    def invoke(self, user_input: str) -> str:
        self.chat_history.add_message("user", user_input)
        messages = self.chat_history.get_messages()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.processed_tools,
            tool_choice=self.tool_choice,
        )
        return self._process_response(response)

    async def ainvoke(self, user_input: str) -> str:
        self.chat_history.add_message("user", user_input)
        messages = self.chat_history.get_messages()
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.processed_tools,
            tool_choice=self.tool_choice,
        )
        return await self._aprocess_response(response)

    def stream_invoke(self, user_input: str) -> Iterator[str]:
        self.chat_history.add_message("user", user_input)
        messages = self.chat_history.get_messages()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.processed_tools,
            tool_choice=self.tool_choice,
            stream=True,
        )
        return self._stream_process_response(response)

    async def astream_invoke(self, user_input: str) -> AsyncIterable[str]:
        self.chat_history.add_message("user", user_input)
        messages = self.chat_history.get_messages()
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.processed_tools,
            tool_choice=self.tool_choice,
            stream=True,
        )
        async for chunk in self._astream_process_response(response):
            yield chunk

    def _process_response(self, response: ChatCompletion) -> str:
        message = response.choices[0].message
        if message.tool_calls:
            self.chat_history.messages.append(message)

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"Calling function {function_name} with args {function_args}")
                try:
                    function_to_call = self.get_tool_function(function_name)
                    result = function_to_call(**function_args)
                except ValueError:
                    result = f"Function '{function_name}' is not implemented."

                self.chat_history.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": str(result),
                    }
                )
            # Make another API call with the updated messages including tool results
            messages = self.chat_history.get_messages()
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            content = response.choices[0].message.content or ""
            self.chat_history.add_message("assistant", content)
            return content
        else:
            content = message.content or ""
            self.chat_history.add_message("assistant", content)
            return content

    def _stream_process_response(
        self, response: Iterator[ChatCompletion]
    ) -> Iterator[str]:
        tool_calls = []  # Accumulator for tool calls to process later
        full_delta_content = ""  # Accumulator for delta content to process later

        for chunk in response:
            if not chunk.choices:
                continue

            delta = (
                chunk.choices[0].delta
                if chunk.choices and chunk.choices[0].delta is not None
                else None
            )
            if delta and delta.content:
                full_delta_content += delta.content
                yield delta.content

            elif delta and delta.tool_calls:
                tc_chunk_list = delta.tool_calls
                for tc_chunk in tc_chunk_list:
                    if len(tool_calls) <= tc_chunk.index:
                        tool_calls.append(
                            {
                                "id": "",
                                "type": "function",
                                "function": {"name": "", "arguments": ""},
                            }
                        )
                    tc = tool_calls[tc_chunk.index]
                    if tc_chunk.id:
                        tc["id"] += tc_chunk.id
                    if tc_chunk.function and tc_chunk.function.name:
                        tc["function"]["name"] += tc_chunk.function.name
                    if tc_chunk.function and tc_chunk.function.arguments:
                        tc["function"]["arguments"] += tc_chunk.function.arguments

        if not tool_calls and full_delta_content:
            self.chat_history.add_message("assistant", full_delta_content)
        elif tool_calls:
            self.chat_history.messages.append(
                {"role": "assistant", "content": None, "tool_calls": tool_calls}
            )

            for tool_call in tool_calls:
                function_name = tool_call["function"]["name"]
                function_args = json.loads(tool_call["function"]["arguments"])
                try:
                    function_to_call = self.get_tool_function(function_name)
                    print(f"Calling function {function_name} with args {function_args}")
                    function_response = function_to_call(**function_args)
                except ValueError:
                    function_response = (
                        f"Function '{function_name}' is not implemented."
                    )

                self.chat_history.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": function_name,
                        "content": str(function_response),
                    }
                )

            messages = self.chat_history.get_messages()
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
            )
            full_response = ""
            for chunk in response:
                for choice in chunk.choices:
                    delta = choice.delta
                    if delta.content:
                        full_response += delta.content
                        yield delta.content

            if full_response:
                self.chat_history.messages.append(
                    {"role": "assistant", "content": full_response}
                )

    async def _astream_process_response(
        self, response: AsyncIterator[ChatCompletion]
    ) -> AsyncIterator[str]:
        tool_calls = []  # Accumulator for tool calls to process later
        full_delta_content = ""  # Accumulator for delta content to process later

        async for chunk in response:
            if not chunk.choices:
                continue

            delta = (
                chunk.choices[0].delta
                if chunk.choices and chunk.choices[0].delta is not None
                else None
            )
            if delta and delta.content:
                full_delta_content += delta.content
                yield delta.content

            elif delta and delta.tool_calls:
                tc_chunk_list = delta.tool_calls
                for tc_chunk in tc_chunk_list:
                    if len(tool_calls) <= tc_chunk.index:
                        tool_calls.append(
                            {
                                "id": "",
                                "type": "function",
                                "function": {"name": "", "arguments": ""},
                            }
                        )
                    tc = tool_calls[tc_chunk.index]
                    if tc_chunk.id:
                        tc["id"] += tc_chunk.id
                    if tc_chunk.function and tc_chunk.function.name:
                        tc["function"]["name"] += tc_chunk.function.name
                    if tc_chunk.function and tc_chunk.function.arguments:
                        tc["function"]["arguments"] += tc_chunk.function.arguments

        if not tool_calls and full_delta_content:
            self.chat_history.messages.append(
                {"role": "assistant", "content": full_delta_content}
            )
        elif tool_calls:
            self.chat_history.messages.append(
                {"role": "assistant", "content": None, "tool_calls": tool_calls}
            )

            for tool_call in tool_calls:
                function_name = tool_call["function"]["name"]
                function_args = json.loads(tool_call["function"]["arguments"])
                try:
                    function_to_call = self.get_tool_function(function_name)
                    print(f"Calling function {function_name} with args {function_args}")
                    function_response = function_to_call(**function_args)
                except ValueError:
                    function_response = (
                        f"Function '{function_name}' is not implemented."
                    )

                self.chat_history.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": function_name,
                        "content": str(function_response),
                    }
                )

            messages = self.chat_history.get_messages()
            async_response = await self.async_client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
            )
            full_response = ""
            async for chunk in async_response:
                for choice in chunk.choices:
                    delta = choice.delta
                    if delta.content:
                        full_response += delta.content
                        yield delta.content

            if full_response:
                self.chat_history.messages.append(
                    {"role": "assistant", "content": full_response}
                )

    async def _aprocess_response(self, response: ChatCompletion) -> str:
        message = response.choices[0].message
        if message.tool_calls:
            self.chat_history.messages.append(message)

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"Calling function {function_name} with args {function_args}")
                try:
                    function_to_call = self.get_tool_function(function_name)
                    result = function_to_call(**function_args)
                except ValueError:
                    result = f"Function '{function_name}' is not implemented."

                self.chat_history.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": str(result),
                    }
                )
            # Make another API call with the updated messages including tool results
            messages = self.chat_history.get_messages()
            response = await self.async_client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            content = response.choices[0].message.content or ""
            self.chat_history.add_message("assistant", content)
            return content
        else:
            content = message.content or ""
            self.chat_history.add_message("assistant", content)
            return content

    def get_history(self) -> List[Dict[str, str]]:
        return self.chat_history.get_messages()

    def clear_history(self) -> None:
        self.chat_history.clear()
