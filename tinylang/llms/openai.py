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
        tool_choice: str | Dict = "auto",
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
        self.tool_choice = tool_choice

    def get_tool_function(self, function_name: str):
        if not self.original_tools:
            raise ValueError("No tools have been set for this chat instance")
        for tool in self.original_tools:
            if tool.name == function_name:
                return tool.function, tool.is_async
        raise ValueError(f"Function {function_name} not found in tools")

    def invoke(self, user_input: Optional[str] = None) -> str:
        if user_input:
            self.chat_history.add_message("user", user_input)
        messages = self.chat_history.get_messages()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.processed_tools,
            tool_choice=self.tool_choice,
        )
        return self._process_response(response)

    async def ainvoke(self, user_input: Optional[str] = None) -> str:
        if user_input:
            self.chat_history.add_message("user", user_input)
        messages = self.chat_history.get_messages()
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.processed_tools,
            tool_choice=self.tool_choice,
        )
        return await self._aprocess_response(response)

    def stream_invoke(self, user_input: Optional[str] = None) -> Iterator[str]:
        if user_input:
            self.chat_history.add_message("user", user_input)
        messages = self.chat_history.get_messages()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.processed_tools,
            tool_choice=self.tool_choice,
            stream=True,
        )
        yield from self._stream_process_response(response)

    async def astream_invoke(
        self, user_input: Optional[str] = None
    ) -> AsyncIterator[str]:
        if user_input:
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
                function_to_call, is_async = self.get_tool_function(function_name)
                if is_async:
                    raise ValueError(
                        "Async tools cannot be used with synchronous methods. Use the async methods instead such as .ainvoke()."
                    )
                result = function_to_call(**function_args)

                self.chat_history.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": str(result),
                    }
                )

            return self.invoke()
        else:
            content = message.content
            self.chat_history.add_message("assistant", content)
            return content

    def _stream_process_response(
        self, response: Iterator[ChatCompletion]
    ) -> Iterator[str]:
        tool_calls = []
        full_content = ""

        for chunk in response:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            if delta.content:
                full_content += delta.content
                yield delta.content

            if delta.tool_calls:
                for tc_chunk in delta.tool_calls:
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

        if tool_calls:
            self.chat_history.messages.append(
                {"role": "assistant", "content": None, "tool_calls": tool_calls}
            )

            for tool_call in tool_calls:
                function_name = tool_call["function"]["name"]
                function_args = json.loads(tool_call["function"]["arguments"])
                function_to_call, is_async = self.get_tool_function(function_name)
                if is_async:
                    raise ValueError(
                        "Async tools cannot be used with synchronous methods. Use the async methods instead such as .astream_invoke()."
                    )
                result = function_to_call(**function_args)

                self.chat_history.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": function_name,
                        "content": str(result),
                    }
                )

            # Recursively call stream_invoke() without passing any user input
            yield from self.stream_invoke()
        else:
            self.chat_history.add_message("assistant", full_content)

    async def _astream_process_response(
        self, response: AsyncIterator[ChatCompletion]
    ) -> AsyncIterator[str]:
        tool_calls = []
        full_content = ""

        async for chunk in response:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            if delta.content:
                full_content += delta.content
                yield delta.content

            if delta.tool_calls:
                for tc_chunk in delta.tool_calls:
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

        if tool_calls:
            self.chat_history.messages.append(
                {"role": "assistant", "content": None, "tool_calls": tool_calls}
            )

            for tool_call in tool_calls:
                function_name = tool_call["function"]["name"]
                function_args = json.loads(tool_call["function"]["arguments"])
                function_to_call, is_async = self.get_tool_function(function_name)
                print(f"Calling function {function_name} with args {function_args}")
                if is_async:
                    result = await function_to_call(**function_args)
                else:
                    result = function_to_call(**function_args)

                self.chat_history.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": function_name,
                        "content": str(result),
                    }
                )

            # Recursively call astream_invoke() without passing any user input
            async for chunk in self.astream_invoke():
                yield chunk
        else:
            self.chat_history.add_message("assistant", full_content)

    async def _aprocess_response(self, response: ChatCompletion) -> str:
        message = response.choices[0].message
        if message.tool_calls:
            self.chat_history.messages.append(message)

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                print(f"Calling function {function_name} with args {function_args}")
                try:
                    function_to_call, is_async = self.get_tool_function(function_name)
                    if is_async:
                        result = await function_to_call(**function_args)
                    else:
                        return function_to_call(**function_args)
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

            # Recursively call ainvoke() without passing any user input
            return await self.ainvoke()
        else:
            content = message.content
            self.chat_history.add_message("assistant", content)
            return content

    def get_history(self) -> List[Dict[str, str]]:
        return self.chat_history.get_messages()

    def clear_history(self) -> None:
        self.chat_history.clear()
