# ChatOpenAI

The `ChatOpenAI` class provides an interface to interact with OpenAI's language models, including support for function calling (tools).

## Initialization

```python
from tinylang.llms import ChatOpenAI
from tinylang.tools import Tool

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

tools = [
    Tool(
        name="multiply",
        description="Multiply two integers",
        function=multiply
    )
]

chat = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=None,  # Optional: Defaults to OPENAI_API_KEY environment variable
    chat_history=10,  # Optional: Number of messages to keep in history
    system_message="You are a helpful assistant.",  # Optional: System message for the conversation
    tools=tools,  # Optional: List of Tool objects for function calling
    tool_choice="auto"  # Optional: How to choose which function to call
)
```

## Methods

### invoke

Synchronous method to get a response from the model.

```python
response = chat.invoke("What is 5 times 3?")
print(response)
```

This might result in the model using the `multiply` function:

```
To calculate 5 times 3, I'll use the multiply function.

5 times 3 equals 15.

Is there anything else you'd like to know?
```

### ainvoke

Asynchronous version of `invoke`.

```python
import asyncio

async def get_response():
    response = await chat.ainvoke("What is 7 times 6?")
    print(response)

asyncio.run(get_response())
```

### stream_invoke

Synchronous method that streams the response.

```python
for chunk in chat.stream_invoke("Calculate 12 times 8 and explain the process."):
    print(chunk, end='', flush=True)
```

### astream_invoke

Asynchronous version of `stream_invoke`.

```python
async def stream_response():
    async for chunk in chat.astream_invoke("What is 15 times 4? Show your work."):
        print(chunk, end='', flush=True)

asyncio.run(stream_response())
```

## Chat History

The `ChatOpenAI` class automatically manages chat history. You can access the current history using:

```python
history = chat.get_history()
print(history)
```

For more details on chat history management, see the [Chat History](chat_history.md) documentation.

## Using Tools (Function Calling)

The `ChatOpenAI` class supports the use of tools (functions) that the model can call when needed. Here's an example of defining and using a more complex tool:

```python
from tinylang.llms import ChatOpenAI
from tinylang.tools import Tool
from typing import List

def calculate_average(numbers: List[float]) -> float:
    """Calculate the average of a list of numbers."""
    return sum(numbers) / len(numbers)

tools = [
    Tool(
        name="calculate_average",
        description="Calculate the average of a list of numbers",
        function=calculate_average
    )
]

chat = ChatOpenAI("gpt-3.5-turbo", tools=tools)

response = chat.invoke("What's the average of 10, 15, and 20?")
print(response)
```

This might result in:

```
To calculate the average of 10, 15, and 20, I'll use the calculate_average function.

The average of 10, 15, and 20 is 15.

Here's how it works:
1. The function takes the list of numbers [10, 15, 20].
2. It calculates the sum of these numbers: 10 + 15 + 20 = 45.
3. Then it divides the sum by the count of numbers (3 in this case): 45 / 3 = 15.

So, the average of 10, 15, and 20 is 15.

Is there anything else you'd like to know?
```

Remember that the availability and behavior of tools may depend on the specific OpenAI model you're using. Always refer to the latest OpenAI documentation for the most up-to-date information on function calling capabilities.
