from typing import Dict, Iterator, AsyncIterable, List, Any, Optional
import json
from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion
from .base import ChatBase
from .util import get_api_key
from ..history import ChatHistory
from ..tools import evaluate_expression


class ChatOpenAI(ChatBase):
    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        init_kwargs: Dict = {},
        system_message: str | None = None,
        chat_history: int = 0,
        previous_history: Optional[List[Dict[str, str]]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[str] = "auto",
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
        self.tools = tools or [
            {
                "type": "function",
                "function": {
                    "name": "evaluate_expression",
                    "description": "Evaluates a mathematical expression and returns the result.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "The mathematical expression to evaluate.",
                            }
                        },
                        "required": ["expression"],
                    },
                },
            }
        ]
        self.tool_choice = tool_choice

    def invoke(self, user_input: str) -> str:
        self.chat_history.add_message("user", user_input)
        messages = self.chat_history.get_messages()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools,
            tool_choice=self.tool_choice,
        )
        return self._process_response(response)

    async def ainvoke(self, user_input: str) -> str:
        self.chat_history.add_message("user", user_input)
        messages = self.chat_history.get_messages()
        response = await self.async_client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools,
            tool_choice=self.tool_choice,
        )
        return self._process_response(response)

    def stream_invoke(self, user_input: str) -> Iterator[str]:
        self.chat_history.add_message("user", user_input)
        messages = self.chat_history.get_messages()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools,
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
            tools=self.tools,
            tool_choice=self.tool_choice,
            stream=True,
        )
        async for chunk in self._astream_process_response(response):
            yield chunk

    def _process_response(self, response: ChatCompletion) -> str:
        message = response.choices[0].message
        if message.tool_calls:
            # add request message to chat history
            self.chat_history.messages.append(message)
            
            # parallel tool calling
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                if function_name == "evaluate_expression":
                    result = evaluate_expression(function_args["expression"])
                else:
                    result = f"Function '{function_name}' is not implemented."
                    
                # Add the tool call result to the chat history
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
        full_content = ""
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta.tool_calls:
                yield f"Calling function: {delta.tool_calls[0].function.name}"
            elif delta.content:
                full_content += delta.content
                yield delta.content

        if full_content:
            self.chat_history.add_message("assistant", full_content)
        else:
            # Process tool calls if any
            self._process_tool_calls(response.choices[0].message)

    async def _astream_process_response(
        self, response: AsyncIterable[ChatCompletion]
    ) -> AsyncIterable[str]:
        full_content = ""
        async for chunk in response:
            delta = chunk.choices[0].delta
            if delta.tool_calls:
                yield f"Calling function: {delta.tool_calls[0].function.name}"
            elif delta.content:
                full_content += delta.content
                yield delta.content

        if full_content:
            self.chat_history.add_message("assistant", full_content)
        else:
            # Process tool calls if any
            await self._aprocess_tool_calls(response.choices[0].message)

    def _process_tool_calls(self, message):
        if message.tool_calls:
            self.chat_history.messages.append(message)
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                if function_name == "evaluate_expression":
                    result = evaluate_expression(function_args["expression"])
                else:
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

    async def _aprocess_tool_calls(self, message):
        if message.tool_calls:
            self.chat_history.messages.append(message)
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                if function_name == "evaluate_expression":
                    result = evaluate_expression(function_args["expression"])
                else:
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

    def get_history(self) -> List[Dict[str, str]]:
        return self.chat_history.get_messages()
