# Tool Usage in Tinylang

Tools in Tinylang allow language models to call specific functions when needed, enhancing their capabilities and allowing for more complex interactions. This document explains how to create, implement, and use both synchronous and asynchronous tools across different chat interfaces in Tinylang.

## Creating Tools

Tools are created using the `Tool` class from the `tinylang.tools` module. Here's the basic structure of a tool:

```python
from tinylang.tools import Tool

def my_function(param1: type1, param2: type2) -> return_type:
    """Function description."""
    # Function implementation
    return result

my_tool = Tool(
    name="my_function_name",
    description="A brief description of what the function does",
    function=my_function
)
```

For asynchronous tools, use an async function:

```python
import asyncio
from tinylang.tools import Tool

async def my_async_function(param1: type1, param2: type2) -> return_type:
    """Async function description."""
    # Async function implementation
    await asyncio.sleep(1)  # Simulating an async operation
    return result

my_async_tool = Tool(
    name="my_async_function_name",
    description="A brief description of what the async function does",
    function=my_async_function
)
```

The `Tool` class automatically infers the function's parameter types and creates an appropriate input model. However, you can also specify a custom input model if needed:

```python
from pydantic import BaseModel

class CustomInputModel(BaseModel):
    param1: type1
    param2: type2

my_tool_with_custom_model = Tool(
    name="my_function_name",
    description="A brief description of what the function does",
    function=my_function,
    input_model=CustomInputModel
)
```

## Implementing Tools in Chat Interfaces

Tools can be implemented in both the `ChatOpenAI` and `ChatClaude` classes. Here's how to initialize a chat interface with tools:


```python
from tinylang.llms import ChatOpenAI
from tinylang.tools import Tool

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

async def fetch_weather(city: str) -> str:
    """Fetch weather for a city."""
    # Simulating an async API call
    await asyncio.sleep(1)
    return f"The weather in {city} is sunny."

tools = [
    Tool(
        name="multiply",
        description="Multiply two integers",
        function=multiply
    ),
    Tool(
        name="fetch_weather",
        description="Fetch weather for a city",
        function=fetch_weather
    )
]

chat = ChatOpenAI(
    model="gpt-3.5-turbo",
    tools=tools,
    tool_choice="auto"
)
```

The `tool_choice` parameter in `ChatOpenAI` determines how the model decides which function to call. Options include:

- `"auto"`: The model decides whether to call a function and which one to call.
- `"none"`: The model is not allowed to call any functions.
- A specific tool name: The model is forced to call the specified function.

## Using Tools in Conversations

Once tools are implemented, you can use them in conversations just like normal chat interactions. The model will automatically decide when to use a tool based on the context of the conversation.

```python
# Synchronous invocation
response = chat.invoke("What is 7 times 8?")
print(response)

# Asynchronous invocation
async def get_weather():
    response = await chat.ainvoke("What's the weather like in New York?")
    print(response)

asyncio.run(get_weather())
```

## Streaming Responses with Tools

Both `ChatOpenAI` and `ChatClaude` support streaming responses, even when using tools:

```python
for chunk in chat.stream_invoke("Calculate 12 times 8 and then get the weather in London."):
    print(chunk, end='', flush=True)

# Asynchronous streaming
async def stream_response():
    async for chunk in chat.astream_invoke("What's 15 times 4? Then check the weather in Tokyo."):
        print(chunk, end='', flush=True)

asyncio.run(stream_response())
```

## Configuring Tool Choice in Chat Interfaces

In the `ChatX` classes, the `tool_choice` parameter determines how the model selects and uses tools. Refer to the appropriate documentation, as this is directly passed into the client when creating a request.

[OpenAI](https://platform.openai.com/docs/guides/function-calling)

[Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/tool-use#controlling-claudes-output)

[Gemini](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling#tool-config)

## Notebook-style Example

Here's a more comprehensive example that you might use in a Jupyter notebook:

```python
import asyncio
from tinylang.llms import ChatOpenAI, ChatClaude
from tinylang.tools import Tool

# Define tools
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

async def fetch_weather(city: str) -> str:
    """Fetch weather for a city."""
    # Simulating an async API call
    await asyncio.sleep(1)
    return f"The weather in {city} is sunny."

tools = [
    Tool(name="multiply", description="Multiply two integers", function=multiply),
    Tool(name="fetch_weather", description="Fetch weather for a city", function=fetch_weather)
]

# Initialize chat interfaces
chat_openai = ChatOpenAI(model="gpt-3.5-turbo", tools=tools, tool_choice="auto")
chat_claude = ChatClaude(model="claude-3-opus-20240229", tools=tools)

# Synchronous example
print("OpenAI synchronous response:")
print(chat_openai.invoke("What is 6 times 7?"))

print("\nClaude synchronous response:")
print(chat_claude.invoke("What is 6 times 7?"))

# Asynchronous example
async def async_example():
    print("\nOpenAI asynchronous response:")
    print(await chat_openai.ainvoke("What's the weather like in Paris?"))
    
    print("\nClaude asynchronous response:")
    print(await chat_claude.ainvoke("What's the weather like in Paris?"))

asyncio.run(async_example())

# Streaming example
print("\nOpenAI streaming response:")
for chunk in chat_openai.stream_invoke("Calculate 9 times 5, then check the weather in Tokyo."):
    print(chunk, end='', flush=True)

print("\n\nClaude streaming response:")
for chunk in chat_claude.stream_invoke("Calculate 9 times 5, then check the weather in Tokyo."):
    print(chunk, end='', flush=True)

# Async streaming example
async def async_streaming_example():
    print("\n\nOpenAI async streaming response:")
    async for chunk in chat_openai.astream_invoke("What's 12 times 3? Then check the weather in London."):
        print(chunk, end='', flush=True)
    
    print("\n\nClaude async streaming response:")
    async for chunk in chat_claude.astream_invoke("What's 12 times 3? Then check the weather in London."):
        print(chunk, end='', flush=True)

asyncio.run(async_streaming_example())
```

This notebook-style example demonstrates how to use both synchronous and asynchronous tools with OpenAI and Claude, including streaming responses.

## Best Practices

1. **Clear Descriptions**: Provide clear and concise descriptions for your tools. This helps the model understand when and how to use them.

2. **Type Annotations**: Always use type annotations in your function definitions. This allows Tinylang to create accurate input models for the tools.

3. **Error Handling**: Implement proper error handling in your tool functions. The chat interface will catch and report errors, but well-handled errors provide better user experience.

4. **Stateless Functions**: Keep your tool functions stateless whenever possible. This ensures consistent behavior across multiple invocations.

5. **Async vs Sync**: Use async functions for I/O-bound operations (like API calls) and sync functions for CPU-bound operations. This helps maintain responsiveness in your application.

6. **Testing**: Thoroughly test your tools independently before integrating them into chat interfaces. Test both synchronous and asynchronous scenarios.

7. **Context Management**: Be mindful of the context when using async tools. Ensure you're in an async context when calling async methods.

Remember that the availability and behavior of tools may depend on the specific model you're using. Always refer to the latest documentation of the language model provider for the most up-to-date information on function calling capabilities.
