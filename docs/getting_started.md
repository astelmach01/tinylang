# Getting Started with Tinylang

## Installation

Install Tinylang using pip:

```bash
pip install tinylang
```

## Configuration

Set up your API keys as environment variables:

- `OPENAI_API_KEY` for OpenAI
- `ANTHROPIC_API_KEY` for Claude
- `GOOGLE_API_KEY` for Gemini

Alternatively, you can pass the API keys directly when initializing the chat interfaces.

## Basic Usage

Here's a simple example using the OpenAI interface:

```python
from tinylang.llms import ChatOpenAI

chat = ChatOpenAI("gpt-3.5-turbo")
response = chat.invoke("Hello, how are you?")
print(response)
```

For more examples and detailed usage instructions, check out the documentation for each chat interface:

- [OpenAI](chat_openai.md)
- [Claude](chat_claude.md)
- [Gemini](chat_gemini.md)
