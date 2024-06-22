# API Reference

This page provides a comprehensive reference for the Tinylang API.

## Chat Interfaces

### ChatOpenAI

```python
class ChatOpenAI:
    def __init__(self, model: str, api_key: Optional[str] = None, chat_history: int = 10, system_message: Optional[str] = None)
    def invoke(self, prompt: str) -> str
    async def ainvoke(self, prompt: str) -> str
    def stream_invoke(self, prompt: str) -> Iterator[str]
    async def astream_invoke(self, prompt: str) -> AsyncIterable[str]
    def get_history(self) -> List[Dict[str, str]]
```

### ChatClaude

```python
class ChatClaude:
    def __init__(self, model: str, api_key: Optional[str] = None, chat_history: int = 10, system_message: Optional[str] = None)
    def invoke(self, prompt: str) -> str
    async def ainvoke(self, prompt: str) -> str
    def stream_invoke(self, prompt: str) -> Iterator[str]
    async def astream_invoke(self, prompt: str) -> AsyncIterable[str]
    def get_history(self) -> List[Dict[str, str]]
```

### ChatGemini

```python
class ChatGemini:
    def __init__(self, model: str, api_key: Optional[str] = None, chat_history: int = 10, system_message: Optional[str] = None)
    def invoke(self, prompt: str) -> str
    async def ainvoke(self, prompt: str) -> str
    def stream_invoke(self, prompt: str) -> Iterator[str]
    async def astream_invoke(self, prompt: str) -> AsyncIterable[str]
    def get_history(self) -> List[Dict[str, str]]
```

## ChatHistory

```python
class ChatHistory:
    def __init__(self, max_history: int, system_message: str, previous_history: Optional[List[Dict[str, str]]] = None)
    def add_message(self, role: str, content: str)
    def get_messages() -> List[Dict[str, str]]
    def clear()
```

For detailed usage instructions and examples, please refer to the individual documentation pages for each class.
