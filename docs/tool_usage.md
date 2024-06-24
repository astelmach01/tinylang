# Tool Usage in Tinylang

Tools in Tinylang allow language models to call specific functions when needed, enhancing their capabilities and allowing for more complex interactions. This document explains how to create, implement, and use tools across different chat interfaces in Tinylang.

## Creating Tools

Tools are created using the `Tool` class from the `tinylang.tools` module. Here's the basic structure of a tool:

```python
from tinylang.tools import Tool

def my_function(param1: type1, param2: type2) -> return_type:
    """Function description."""
    # Function implementation
    return result

my_tool = Tool(
    name="my_function_name",
    description="A brief description of what the function does",
    function=my_function
)
```

The `Tool` class automatically infers the function's parameter types and creates an appropriate input model. However, you can also specify a custom input model if needed:

```python
from pydantic import BaseModel

class CustomInputModel(BaseModel):
    param1: type1
    param2: type2

my_tool_with_custom_model = Tool(
    name="my_function_name",
    description="A brief description of what the function does",
    function=my_function,
    input_model=CustomInputModel
)
```

## Implementing Tools in Chat Interfaces

Currently, tool usage is primarily implemented in the `ChatOpenAI` class. Here's how to initialize a chat interface with tools:

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
    tools=tools,
    tool_choice="auto"
)
```

The `tool_choice` parameter determines how the model decides which function to call. Options include:

- `"auto"`: The model decides whether to call a function and which one to call.
- `"none"`: The model is not allowed to call any functions.
- A specific tool name: The model is forced to call the specified function.

## Using Tools in Conversations

Once tools are implemented, you can use them in conversations just like normal chat interactions. The model will automatically decide when to use a tool based on the context of the conversation.

```python
response = chat.invoke("What is 7 times 8?")
print(response)
```

This might result in:

```
To calculate 7 times 8, I'll use the multiply function.

7 times 8 equals 56.

Is there anything else you'd like to know?
```

## Complex Tool Example

Here's an example of a more complex tool that calculates statistics for a list of numbers:

```python
from tinylang.llms import ChatOpenAI
from tinylang.tools import Tool
from typing import List
import statistics

def calculate_stats(numbers: List[float]) -> dict:
    """Calculate various statistics for a list of numbers."""
    return {
        "mean": statistics.mean(numbers),
        "median": statistics.median(numbers),
        "stdev": statistics.stdev(numbers) if len(numbers) > 1 else None
    }

tools = [
    Tool(
        name="calculate_stats",
        description="Calculate mean, median, and standard deviation for a list of numbers",
        function=calculate_stats
    )
]

chat = ChatOpenAI("gpt-3.5-turbo", tools=tools)

response = chat.invoke("What are the mean, median, and standard deviation of 10, 15, 20, 25, and 30?")
print(response)
```

This might result in:

```
To calculate the statistics for the numbers 10, 15, 20, 25, and 30, I'll use the calculate_stats function.

Here are the results:

1. Mean: 20.0
   The mean is the average of all numbers. (10 + 15 + 20 + 25 + 30) / 5 = 20.0

2. Median: 20.0
   The median is the middle number when the list is sorted. In this case, it's 20.

3. Standard Deviation: approximately 7.91
   The standard deviation measures the amount of variation in the dataset.

These statistics provide insights into the central tendency (mean and median) and spread (standard deviation) of the given numbers.

Is there anything else you'd like to know about these numbers or any other statistical calculations?
```

## Best Practices

1. **Clear Descriptions**: Provide clear and concise descriptions for your tools. This helps the model understand when and how to use them.

2. **Type Annotations**: Always use type annotations in your function definitions. This allows Tinylang to create accurate input models for the tools.

3. **Error Handling**: Implement proper error handling in your tool functions. The chat interface will catch and report errors, but well-handled errors provide better user experience.

4. **Stateless Functions**: Keep your tool functions stateless whenever possible. This ensures consistent behavior across multiple invocations.

5. **Testing**: Thoroughly test your tools independently before integrating them into chat interfaces.

Remember that the availability and behavior of tools may depend on the specific model you're using. Always refer to the latest documentation of the language model provider for the most up-to-date information on function calling capabilities.
