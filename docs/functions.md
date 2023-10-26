# Working with Functions in Tinylang

## Introduction

Functions in Tinylang enable you to define callable operations with metadata. These functions can be used in conjunction with chat models to extend their capabilities.

🚧 **Note**: Functions and Agents are under active development. This is the intended API and passing functions into LLMs is not supported yet. 🚧

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

@function
def subtract(a: int, b: int):
    """
    Subtracts two numbers
    """
    return a - b



functions = [add, subtract]
print(functions)
```

```
[{'name': 'add',
  'description': '\n    Adds two numbers\n    ',
  'parameters': {'properties': {'a': {'type': 'integer'},
    'b': {'type': 'integer'}},
   'required': ['a', 'b'],
   'type': 'object'}},
 {'name': 'subtract',
  'description': '\n    Subtracts two numbers\n    ',
  'parameters': {'properties': {'a': {'type': 'integer'},
    'b': {'type': 'integer'}},
   'required': ['a', 'b'],
   'type': 'object'}}]
```

## Using Functions with Chat Models

The `functions` parameter can be passed into the kwargs of the `.chat` method, making it visible to the LLM. If the LLM chooses the call the function, then it will output accompanying parameters to call.


```python
from tinylang.llms import OpenAI

chatGPT = OpenAI(
    openai_api_key="",
    openai_organization="",
    model="gpt-3.5-turbo",
)

chatGPT.chat("hello", functions=functions)
```

Note that the API will not actually execute any function calls. It is up to developers to execute function calls using model outputs.

## Next Steps

- Learn how to [work with Images](images.md)
- Dive into [Memory Management with ConversationMemory](conversation_memory.md)
