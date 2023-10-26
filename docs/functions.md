# Working with Functions in Tinylang

## Introduction

Functions in Tinylang enable you to define callable operations with metadata. These functions can be used in conjunction with chat models to extend their capabilities.

🚧 **Note**: Functions and Agents are under active development. This is the intended API and does not work yet. 🚧

## Defining a Function

To define a function, use the `@function` decorator. The function should take named arguments and can include a docstring for description.

```python
from tinylang.functions import function

@function
def add(a: int, b: int):
    """
    Adds two numbers
    """
    return a + b
```

## Function Metadata

Once defined, the function metadata can be accessed as follows:

```python
functions = [add]
print(functions)
```

This will output a list containing the function metadata, including name, description, and parameters.

## Using Functions with Chat Models

The `functions` parameter in the Chat Completion API can be used to provide function specifications. The chat model can then generate function arguments that adhere to these specifications.

```python
functions = [
    {
        "name": "add",
        "description": "Adds two numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"}
            },
            "required": ["a", "b"]
        }
    }
]
```

Note that the API will not actually execute any function calls. It is up to developers to execute function calls using model outputs.

## Next Steps

- Learn how to [work with Images](images.md)
- Dive into [Memory Management with ConversationMemory](conversation_memory.md)
