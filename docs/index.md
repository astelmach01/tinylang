# Welcome to Tinylang

Tinylang is a Python library that provides a unified interface for interacting with various Large Language Models (LLMs) including OpenAI's GPT, Anthropic's Claude, and Google's Gemini.

## Features

- Unified API for multiple LLM providers
- Support for OpenAI, Anthropic Claude, and Google Gemini
- Synchronous and asynchronous invocation methods
- Streaming support for real-time responses
- Chat history management
- Easy integration with existing projects

## Quick Start

Install Tinylang:

```bash
pip install tinylang
```

Basic usage:

```python
from tinylang.llms import ChatOpenAI

chat = ChatOpenAI("gpt-3.5-turbo")
response = chat.invoke("Hello, how are you?")
print(response)
```

For more detailed information, check out our [Getting Started](getting_started.md) guide.
