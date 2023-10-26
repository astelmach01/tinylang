# Working with Chains in Tinylang

## Introduction

Chains in Tinylang serve as the primary interface for interacting with Langchain. This guide will walk you through the basics of setting up and using Chains.

## Initialize a Chain

To initialize a Chain, you'll need an instance of a Large Language Model (LLM) and optionally, a Memory object.

```python
from tinylang.chains import Chain
from tinylang.llms import OpenAI
from tinylang.memory import ConversationMemory


chatGPT = OpenAI(
    openai_api_key='',
    openai_organization='',
    model="gpt-3.5-turbo",
)

memory = ConversationMemory(last_k=5)
chain = Chain(llm, memory)
```

## Run a Chain

Running a Chain is as simple as calling the `run` method with a prompt.

```python
response = chain.run("Hello, world!")
```

## Next Steps

- Learn how to [work with Functions](functions.md)
- Dive into [Conversation Memory](conversation_memory.md)
