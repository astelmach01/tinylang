# Working with Conversation Memory in Tinylang

## Introduction

Conversation Memory in Tinylang is a crucial component for managing the flow of messages between the user and the assistant. This guide will walk you through how to use and manipulate conversation memory.


## Initialization

To initialize a Conversation Memory, you can specify the `last_k` parameter to limit the number of stored messages. This defines how many interactions are stored, where an interaction is defined as (user, assistant) pair.

```python
from tinylang.memory import ConversationMemory

memory = ConversationMemory(last_k=4)
```

## Adding Messages

You can add different types of messages to the conversation memory.

```python
from tinylang.messages import UserMessage, AssistantMessage, SystemMessage


memory.add_system_message("You are an expert programmer")
memory.add_user_message("Hi")
memory.add_assistant_message("Hello")
```

## Accessing Messages

You can access the stored messages and their metadata.

```python
print(memory.messages)
```

Specifically, using `.format_messages()` formats it to pass into an OpenAI ChatCompletion endpoint.

```python
print(memory.format_messages())
```

## Message Limitation

The `last_k` parameter limits the number of stored messages to the last `2 * last_k` messages. Set last_k to `None` if you'd like to keep all messages.

```python
cm = ConversationMemory(last_k=4)
for i in range(20):
    cm.add_user_message(f"Message {i}")
    cm.add_system_message(f"Message AI {i}")
assert len(cm.messages) == 8
```

## Advanced Features

You can also include images in the messages and store them in the conversation memory.

```python
from tinylang.images import Image
import numpy as np

image_data = np.array([[0, 1], [1, 0]])
user_image = Image(image_data)
memory.add_message(UserMessage(content="What is this?", image=user_image))
```

## Next Steps

- Learn how to [work with Functions](functions.md)
- Dive into [Working with Images](images.md)
