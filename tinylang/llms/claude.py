from typing import Dict, Iterator, AsyncIterable, List, Optional, Any
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
        tool_choice: Optional[str] = None,
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
        self.tool_choice = tool_choice if tools else None

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
                return tool.function

        raise ValueError(f"Tool {function_name} not found.")

    def invoke(self, prompt: str, max_tokens: int = 2048) -> str:
        self.chat_history.add_message("user", prompt)
        messages = self.chat_history.get_messages()[1:]  # Exclude system message
        response = self.client.messages.create(
            model=self.model,
            system=self.system_message,
            max_tokens=max_tokens,
            messages=messages,
            tools=self.processed_tools,
        )
        return self._process_response(response)

    async def ainvoke(self, prompt: str) -> str:
        self.chat_history.add_message("user", prompt)
        messages = self.chat_history.get_messages()[1:]  # Exclude system message
        response = await self.async_client.messages.create(
            model=self.model,
            system=self.system_message,
            max_tokens=2048,
            messages=messages,
            tools=self.processed_tools,
        )
        content = response.content[0].text or ""
        self.chat_history.add_message("assistant", content)
        return content

    def stream_invoke(self, prompt: str) -> Iterator[str]:
        self.chat_history.add_message("user", prompt)
        messages = self.chat_history.get_messages()[1:]  # Exclude system message
        with self.client.messages.stream(
            model=self.model,
            system=self.system_message,
            max_tokens=2048,
            messages=messages,
        ) as stream:
            for event in stream:
                if event.type == "text":
                    yield event.text

            final_message = stream.get_final_message()
            self.chat_history.add_message("assistant", final_message.content)

            tool_calls = [
                block
                for block in final_message.content
                if isinstance(block, ToolUseBlock)
            ]

            tool_response_content = []

            for tool_call in tool_calls:
                function_name = tool_call.name
                function_args = tool_call.input
                try:
                    function_to_call = self.get_tool_function(function_name)
                    print(f"Calling function {function_name} with args {function_args}")
                    function_response = function_to_call(**function_args)

                    tool_result = {
                        "type": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": str(function_response),
                    }

                    tool_response_content.append(tool_result)
                except Exception as e:
                    print(f"Error calling function {function_name}: {str(e)}")

            # Append tool responses to messages as a user message
            if tool_response_content:
                self.chat_history.add_message("user", tool_response_content)

            if tool_calls:
                with self.client.messages.stream(
                    max_tokens=2048,
                    model=self.model,
                    system=self.system_message,
                    messages=self.chat_history.get_messages()[1:],
                    tools=self.processed_tools,
                ) as follow_up_stream:
                    for event in follow_up_stream:
                        if event.type == "text":
                            yield event.text

                    final_message = follow_up_stream.get_final_message()
                    self.chat_history.add_message("assistant", final_message.content)

    async def astream_invoke(self, prompt: str) -> AsyncIterable[str]:
        self.chat_history.add_message("user", prompt)
        messages = self.chat_history.get_messages()[1:]  # Exclude system message
        async with self.async_client.messages.stream(
            model=self.model,
            system=self.system_message,
            max_tokens=2048,
            messages=messages,
            tools=self.processed_tools,
        ) as stream:
            async for event in stream:
                if event.type == "text":
                    yield event.text

            final_message = await stream.get_final_message()
            self.chat_history.add_message("assistant", final_message.content)

            tool_calls = [
                block
                for block in final_message.content
                if isinstance(block, ToolUseBlock)
            ]

            tool_response_content = []

            for tool_call in tool_calls:
                function_name = tool_call.name
                function_args = tool_call.input
                try:
                    function_to_call = self.get_tool_function(function_name)
                    print(f"Calling function {function_name} with args {function_args}")
                    function_response = function_to_call(**function_args)

                    tool_result = {
                        "type": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": str(function_response),
                    }

                    tool_response_content.append(tool_result)
                except Exception as e:
                    print(f"Error calling function {function_name}: {str(e)}")

            # Append tool responses to messages as a user message
            if tool_response_content:
                self.chat_history.add_message("user", tool_response_content)

            if tool_calls:
                async with self.async_client.messages.stream(
                    max_tokens=2048,
                    model=self.model,
                    system=self.system_message,
                    messages=self.chat_history.get_messages()[1:],
                    tools=self.processed_tools,
                ) as follow_up_stream:
                    async for event in follow_up_stream:
                        if event.type == "text":
                            yield event.text

                    final_message = await follow_up_stream.get_final_message()
                    self.chat_history.add_message("assistant", final_message.content)

    def _process_response(self, response) -> str:
        if response.stop_reason == "tool_use":
            self.chat_history.add_message("assistant", response.content)
            for message in response.content:
                if message.type == "tool_use":
                    tool_id = message.id
                    tool_name = message.name
                    tool_arguments = message.input
                    tool_function = self.get_tool_function(tool_name)
                    print(f"Calling tool {tool_name} with args {tool_arguments}")
                    try:
                        tool_response = tool_function(**tool_arguments)
                    except Exception as e:
                        print(f"Error calling {tool_function}: {e}")
                        tool_response = f"Error: {e}"

                    self.chat_history.messages.append(
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_id,
                                    "content": str(tool_response),
                                }
                            ],
                        }
                    )

            # make another api call to get the response after the tool has been used
            response = self.client.messages.create(
                model=self.model,
                system=self.system_message,
                max_tokens=2048,
                messages=self.chat_history.get_messages()[1:],  # Exclude system message
                tools=self.processed_tools,
            )
            content = response.content[0].text or ""
            self.chat_history.add_message("assistant", content)
            return content
        else:
            content = response.content[0].text or ""
            self.chat_history.add_message("assistant", content)
            return content

    def get_history(self) -> List[Dict[str, str]]:
        return self.chat_history.get_messages()

    def clear_history(self) -> None:
        self.chat_history.clear()
