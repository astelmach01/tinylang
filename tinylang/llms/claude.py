from typing import Dict, Iterator, AsyncIterable, List, Optional, Any, AsyncIterator
import re
from .base import ChatBase
import anthropic
from anthropic import AsyncAnthropic
from anthropic.types import ToolUseBlock
from .util import get_api_key
from ..history import ChatHistory
from ..tools.tool import Tool, process_tools


class ChatClaude(ChatBase):
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
        api_key = get_api_key(api_key, "ANTHROPIC_API_KEY")
        init_kwargs.update({"api_key": api_key})
        self.client = anthropic.Anthropic(**init_kwargs)
        self.async_client = AsyncAnthropic(**init_kwargs)
        self.model = model
        self.system_message = system_message or "You are a helpful assistant."
        self.chat_history = ChatHistory(
            chat_history, self.system_message, previous_history
        )
        self.original_tools = tools
        self.processed_tools = self._process_tools(tools)
        self.tool_choice = tool_choice

    def _process_tools(
        self, tools: Optional[List[Tool]]
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Process the provided tools and format them according to Claude's specifications.

        Args:
            tools (Optional[List[Tool]]): A list of Tool objects to be processed, or None.

        Returns:
            Optional[List[Dict[str, Any]]]: A list of dictionaries representing the processed tools, or None if no tools were provided.
        """
        if not tools:
            return None

        processed_tools = []
        for tool in tools:
            processed_tool = {
                "name": tool.name,
                "description": tool.description,
                "input_schema": {"type": "object", "properties": {}, "required": []},
            }

            # Ensure the tool name matches Claude's regex requirement
            if not re.match(r"^[a-zA-Z0-9_-]{1,64}$", tool.name):
                raise ValueError(
                    f"Tool name '{tool.name}' does not match the required format."
                )

            # Process input schema
            tool_dict = tool.to_dict()
            for param_name, param_info in tool_dict["function"]["parameters"][
                "properties"
            ].items():
                processed_tool["input_schema"]["properties"][param_name] = {
                    "type": param_info["type"],
                    "description": param_info.get("description", ""),
                }

                # Handle enums
                if "enum" in param_info:
                    processed_tool["input_schema"]["properties"][param_name]["enum"] = (
                        param_info["enum"]
                    )

                # Add to required list if the field is required
                if param_name in tool_dict["function"]["parameters"].get(
                    "required", []
                ):
                    processed_tool["input_schema"]["required"].append(param_name)

            processed_tools.append(processed_tool)

        return processed_tools

    def get_tool_function(self, function_name: str):
        if not self.original_tools:
            raise ValueError("No tools provided.")

        for tool in self.original_tools:
            if tool.name == function_name:
                return tool.function, tool.is_async

        raise ValueError(f"Tool {function_name} not found.")

    def invoke(self, prompt: Optional[str] = None, max_tokens: int = 2048) -> str:
        if prompt is not None:
            self.chat_history.add_message("user", prompt)
        messages = self.chat_history.get_messages()[1:]  # Exclude system message
        response = self.client.messages.create(
            model=self.model,
            system=self.system_message,
            max_tokens=max_tokens,
            messages=messages,
            tools=self.processed_tools,
            tool_choice=self.tool_choice,
        )
        return self._process_response(response)

    async def ainvoke(self, prompt: Optional[str] = None) -> str:
        if prompt is not None:
            self.chat_history.add_message("user", prompt)
        messages = self.chat_history.get_messages()[1:]  # Exclude system message
        response = await self.async_client.messages.create(
            model=self.model,
            system=self.system_message,
            max_tokens=2048,
            messages=messages,
            tools=self.processed_tools,
            tool_choice=self.tool_choice,
        )
        return await self._process_async_response(response)

    def stream_invoke(self, prompt: Optional[str] = None) -> Iterator[str]:
        if prompt is not None:
            self.chat_history.add_message("user", prompt)
        messages = self.chat_history.get_messages()[1:]  # Exclude system message
        with self.client.messages.stream(
            model=self.model,
            system=self.system_message,
            max_tokens=2048,
            messages=messages,
            tools=self.processed_tools,
            tool_choice=self.tool_choice,
        ) as stream:
            yield from self._stream_process_response(stream)

    async def astream_invoke(self, prompt: Optional[str] = None) -> AsyncIterable[str]:
        if prompt is not None:
            self.chat_history.add_message("user", prompt)
        messages = self.chat_history.get_messages()[1:]  # Exclude system message
        async with self.async_client.messages.stream(
            model=self.model,
            system=self.system_message,
            max_tokens=2048,
            messages=messages,
            tools=self.processed_tools,
            tool_choice=self.tool_choice,
        ) as stream:
            async for chunk in self._astream_process_response(stream):
                yield chunk

    def _process_response(self, response) -> str:
        if response.stop_reason == "tool_use":
            self.chat_history.add_message("assistant", str(response.content))

            tool_response_content = []

            for res in response.content:
                if res.type != "tool_use":
                    continue

                tool_id = res.id
                tool_name = res.name
                tool_input = res.input

                function, is_async = self.get_tool_function(tool_name)
                if is_async:
                    raise ValueError(
                        "Async tools cannot be used with synchronous methods, use ainvoke() instead."
                    )
                print(f"Calling function {tool_name} with args {tool_input}")
                result = function(**tool_input)

                tool_response = {
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": str(result),
                }

                tool_response_content.append(tool_response)

            self.chat_history.add_message("user", str(tool_response_content))

            # Recursively call invoke() without passing any user input
            return self.invoke()
        else:
            content = response.content[0].text or ""
            self.chat_history.add_message("assistant", content)
            return content

    async def _process_async_response(self, response) -> str:
        if response.stop_reason == "tool_use":
            self.chat_history.add_message("assistant", str(response.content))

            tool_response_content = []

            for res in response.content:
                if res.type != "tool_use":
                    continue

                tool_id = res.id
                tool_name = res.name
                tool_input = res.input

                function, is_async = self.get_tool_function(tool_name)
                print(f"Calling function {tool_name} with args {tool_input}")
                if is_async:
                    result = await function(**tool_input)
                else:
                    result = function(**tool_input)

                tool_response = {
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": str(result),
                }

                tool_response_content.append(tool_response)

            self.chat_history.add_message("user", str(tool_response_content))

            # Recursively call ainvoke() without passing any user input
            return await self.ainvoke()
        else:
            content = response.content[0].text or ""
            self.chat_history.add_message("assistant", content)
            return content

    def _stream_process_response(self, stream) -> Iterator[str]:
        full_content = ""
        for event in stream:
            if event.type == "text":
                full_content += event.text
                yield event.text

        final_message = stream.get_final_message()
        self.chat_history.add_message("assistant", full_content)

        tool_calls = [
            block for block in final_message.content if isinstance(block, ToolUseBlock)
        ]

        if tool_calls:
            tool_response_content = []

            for tool_call in tool_calls:
                function_name = tool_call.name
                function_args = tool_call.input

                function_to_call, is_async = self.get_tool_function(function_name)
                if is_async:
                    raise ValueError(
                        "Async tools cannot be used with synchronous methods, use astream_invoke() instead."
                    )
                print(f"Calling function {function_name} with args {function_args}")
                function_response = function_to_call(**function_args)

                tool_result = {
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": str(function_response),
                }

                tool_response_content.append(tool_result)

            self.chat_history.add_message("user", str(tool_response_content))

            # Recursively call stream_invoke() without passing any user input
            yield from self.stream_invoke()

    async def _astream_process_response(self, stream) -> AsyncIterator[str]:
        full_content = ""
        async for event in stream:
            if event.type == "text":
                full_content += event.text
                yield event.text

        final_message = await stream.get_final_message()
        self.chat_history.add_message("assistant", full_content)

        tool_calls = [
            block for block in final_message.content if isinstance(block, ToolUseBlock)
        ]

        if tool_calls:
            tool_response_content = []

            for tool_call in tool_calls:
                function_name = tool_call.name
                function_args = tool_call.input
                function_to_call, is_async = self.get_tool_function(function_name)

                print(f"Calling function {function_name} with args {function_args}")
                if is_async:
                    function_response = await function_to_call(**function_args)
                else:
                    function_response = function_to_call(**function_args)

                tool_result = {
                    "type": "tool_result",
                    "tool_use_id": tool_call.id,
                    "content": str(function_response),
                }

                tool_response_content.append(tool_result)

            self.chat_history.add_message("user", str(tool_response_content))

            # Recursively call astream_invoke() without passing any user input
            async for chunk in self.astream_invoke():
                yield chunk

    def get_history(self) -> List[Dict[str, str]]:
        return self.chat_history.get_messages()

    def clear_history(self) -> None:
        self.chat_history.clear()
