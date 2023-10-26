# 🚀 Getting Started with Tinylang

## 📋 Prerequisites

- 🐍 Python 3.x
- 📦 pip (Python package installer)

To install Tinylang, run:

```bash
pip install tinylang
```

## 🐍 Installing Python

If you don't have Python installed, you can download it from the [🌐 official Python website](https://www.python.org/downloads/).

### On macOS and Linux:

You can also use package managers like `brew` on macOS:

```bash
brew install python3
```

Or `apt` on Ubuntu:

```bash
sudo apt update
sudo apt install python3
```

### On Windows:

Download the installer from the [🌐 official Python website](https://www.python.org/downloads/windows/) and follow the installation instructions.

## Installing pip

If you don't have pip installed, you can install it as follows:

### On macOS and Linux:

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

### On Windows:

Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) to a folder on your computer. Open a command prompt from within the Start menu, navigate to the folder containing `get-pip.py`, and run:

```bash
python get-pip.py
```

## Quick Start

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

## Next Steps

- [⛓️ Working with Chains](chains.md)
- [🔧 Working with Functions](functions.md)
- [🖼️ Working with Images](images.md)
- [🧠 Conversation Memory](conversation_memory.md)
