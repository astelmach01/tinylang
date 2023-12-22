# 🦜🔗🔍 Tinylang
[Documentation](https://astelmach01.github.io/tinylang/)

## This is deprecated, use [OpenAI Assistants](https://platform.openai.com/docs/assistants/overview) instead.

Make working with LLMs insanely simpler and easier than ever before.

## What is tinylang?
A hackable and simpler Langchain.

Langchain can be very cumbersome and annoying to work with. It's too big, complicated, and shoves pre-made prompts down your throat.

With tinylang, everything is intuitive and customizable, following most of the Langchain API.


## Installation

```shell
pip install tinylang
```

## Usage


```python
from tinylang.chains import Chain
from tinylang.llms import OpenAI
from tinylang.memory import ConversationMemory

model = "gpt-3.5-turbo"

chatGPT = OpenAI(
    openai_api_key=openai_api_key,
    openai_organization=openai_organization,
    model=model,
)

memory = ConversationMemory()

chain = Chain(
    llm=chatGPT,
    memory=memory,
)

prompt = "Hello"
print(chain.run(prompt))
```


## Features

- 🧠 Conversation Memory. Keep all or some aspects of your conversation
- 🛸 OpenAI LLMs. It couldn't be easier to call the OpenAI API.
- 💻 Prompts. Simple and hackable.
- 🤖 Agents. Coming soon!
