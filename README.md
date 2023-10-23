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



## Contributing

To automate package versions, we use semantic-release, which automatically bumps versions based on our commit messages.
See [here](https://py-pkgs.org/07-releasing-versioning.html#automatic-version-bumping).

Example: add a feature, minor version will be bumped from `0.1.0` to `0.2.0`:
```
git commit -m "feat: add example data and datasets module"
```

Example: fix a bug, patch version bumped from `0.1.0` to `0.1.1`
```
git commit -m "fix: fix confusing error message in plot_words"
```
