# 🦜🔗🔍 Tinylang

Tinylang is a Python library that provides a unified interface for interacting with various Large Language Models (LLMs) including OpenAI's GPT, Anthropic's Claude, and Google's Gemini.

[Documentation](https://astelmach01.github.io/tinylang/)

## Features

- Unified API for multiple LLM providers
- Support for OpenAI, Anthropic Claude, and Google Gemini
- Synchronous and asynchronous invocation methods
- Streaming support for real-time responses
- Chat history management
- Easy integration with existing projects

## Installation

To install Tinylang, use pip:

```bash
pip install tinylang
```

## Usage

Here's a quick example of how to use Tinylang:

```python
from tinylang.llms import ChatOpenAI, ChatClaude, ChatGemini

# Initialize chat interfaces
openai_chat = ChatOpenAI("gpt-4o", chat_history=2)
claude_chat = ChatClaude("claude-3-opus-20240229", chat_history=2)
gemini_chat = ChatGemini("gemini-1.5-pro", chat_history=2)

# Use the chat interfaces
response = openai_chat.invoke("Hello, how are you?")
print(response)

# Streaming example
for chunk in claude_chat.stream_invoke("Tell me a joke"):
    print(chunk, end='')

# Async example
async def async_chat():
    response = await gemini_chat.ainvoke("What's the weather like today?")
    print(response)

# Run the async function
import asyncio
asyncio.run(async_chat())
```

## API Reference

### ChatOpenAI, ChatClaude, ChatGemini

These classes provide interfaces to their respective LLM providers. They share the following methods:

- `invoke(prompt: str) -> str`: Synchronous invocation
- `ainvoke(prompt: str) -> str`: Asynchronous invocation
- `stream_invoke(prompt: str) -> Iterator[str]`: Synchronous streaming invocation
- `astream_invoke(prompt: str) -> AsyncIterable[str]`: Asynchronous streaming invocation

### ChatHistory

Manages the conversation history for the chat interfaces.

## Configuration

Set the following environment variables for API authentication:

- `OPENAI_API_KEY` for OpenAI
- `ANTHROPIC_API_KEY` for Claude
- `GOOGLE_API_KEY` for Gemini

Alternatively, you can pass the API keys directly when initializing the chat interfaces.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## More Information

For more detailed information about using Tinylang, please refer to our [documentation](https://astelmach01.github.io/tinylang/).

## To be Added

- tool choice in claude and openai 
- better docs
- infinite, or 0 length chat history
- update gemini
- refactor code
- return structured output
