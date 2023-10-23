# 🦜🔗🔍 Tinylang

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

See `examples` as well!

```
from tinychain.memory import ConversationMemory
from tinychain.llms import OpenAI
from tinychain.chains import Chain

memory = ConversationMemory(last_k=10)

chatGPT = OpenAI(openai_api_key='')

chain = Chain(memory, chatGPT)

prompt = "Hello"
print(chain.run(prompt))
```


## Features

- 🧠 Conversation Memory. Keep all or some aspects of your conversation
- 🤖 OpenAI LLMs. It couldn't be easier to call the OpenAI API.
- 💻 Prompts. Simple and hackable.
