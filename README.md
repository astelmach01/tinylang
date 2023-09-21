# 🦜🔗🔍 Tinylang

Make working with LLMs insanely simpler and easier than ever before.

## What is tinylang?
A hackable and simpler Langchain.

Langchain can be very cumbersome and annoying to work with. It's too big, complicated, and shoves premade prompts down your throat.

With tinylang, everything is intuitive and customizeable, following most of the Langchain API.


## Installation

Just pip install with:

```shell
pip install tinylang
```

## Usage

```
from tinychain.memory import ConversationMemory
from tinychain.llms import OpenAIChat
from tinychain.chain import LLMChain

memory = ConversationMemory(last_k=10)

chatGPT = OpenAIChat(OPENAI_API_KEY='')

chain = LLMChain(memory, chatGPT)

prompt = "Hello"
print(chain.run(prompt))
```
