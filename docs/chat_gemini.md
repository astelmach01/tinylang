# ChatGemini

The `ChatGemini` class provides an interface to interact with Google's Gemini language models.

## Initialization

```python
from tinylang.llms import ChatGemini

chat = ChatGemini(
    model="gemini-1.5-pro",
    api_key=None,  # Optional: Defaults to GOOGLE_API_KEY environment variable
    chat_history=10,  # Optional: Number of messages to keep in history
    system_message="You are a helpful assistant."  # Optional: System message for the conversation
)
```

## Methods

### invoke

Synchronous method to get a response from the model.

```python
response = chat.invoke("What is the capital of France?")
print(response)
```

### ainvoke

Asynchronous version of `invoke`.

```python
import asyncio

async def get_response():
    response = await chat.ainvoke("What is the capital of France?")
    print(response)

asyncio.run(get_response())
```

### stream_invoke

Synchronous method that streams the response.

```python
for chunk in chat.stream_invoke("Tell me a story"):
    print(chunk, end='', flush=True)
```

### astream_invoke

Asynchronous version of `stream_invoke`.

```python
async def stream_response():
    async for chunk in chat.astream_invoke("Tell me a story"):
        print(chunk, end='', flush=True)

asyncio.run(stream_response())
```

## Chat History

The `ChatGemini` class automatically manages chat history. You can access the current history using:

```python
history = chat.chat_history.get_messages()
print(history)
```

For more details on chat history management, see the [Chat History](chat_history.md) documentation.
