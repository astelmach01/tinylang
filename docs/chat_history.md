# Chat History

Tinylang provides built-in chat history management for all its chat interfaces. This allows for maintaining context across multiple interactions with the language models.

## How It Works

Each chat interface (`ChatOpenAI`, `ChatClaude`, and `ChatGemini`) maintains its own chat history using the `ChatHistory` class. The history includes all user inputs and model responses, as well as the initial system message.

## Configuring Chat History

When initializing a chat interface, you can specify the number of messages to keep in the history:

```python
from tinylang.llms import ChatOpenAI

chat = ChatOpenAI("gpt-3.5-turbo", chat_history=5)
```

This will keep the last 5 user-model message pairs in the history, in addition to the system message.

## Accessing Chat History

You can access the current chat history at any time using the `get_messages()` method:

```python
history = chat.chat_history.get_messages()
print(history)
```

This returns a list of dictionaries, where each dictionary represents a message with 'role' and 'content' keys.

## Clearing Chat History

To clear the chat history:

```python
chat.chat_history.clear()
```

## Using Previous History

You can initialize a chat interface with a previous history:

```python
previous_history = [
    {"role": "user", "content": "Hello, I am Andrew"},
    {"role": "assistant", "content": "Hello Andrew! How can I assist you today?"},
]

chat = ChatOpenAI("gpt-3.5-turbo", chat_history=5, previous_history=previous_history)
```

This allows you to continue conversations from a previous session or set up specific contexts for your interactions.

## Accessing Chat History

You can access the current chat history at any time using the get_history() method available in all chat interfaces:

```python
history = chat.get_history()
print(history)
```

This returns a list of dictionaries, where each dictionary represents a message with 'role' and 'content' keys.
Alternatively, you can still access the chat history directly through the chat_history attribute:

```python
history = chat.chat_history.get_messages()
print(history)
```

Both methods return the same result.

## Impact on Model Responses

The chat history provides context for the language model, allowing it to generate more relevant and coherent responses across multiple turns of conversation. However, be aware that using a large chat history can increase the token count of your requests, potentially affecting performance and costs.
