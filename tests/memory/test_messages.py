import pytest

from tinylang.memory import ConversationMemory
from tinylang.messages import AssistantMessage, UserMessage


def test_last_k_validation() -> None:
    with pytest.raises(ValueError):
        ConversationMemory._last_k_validation(0)
    assert ConversationMemory._last_k_validation(1) == 1
    assert ConversationMemory._last_k_validation(None) is None


def test_add_message() -> None:
    memory = ConversationMemory(last_k=2)
    assert len(memory.messages) == 0
    memory.add_message(UserMessage("Hello, world!"))
    assert len(memory.messages) == 1
    memory.add_message(AssistantMessage("Hello, world!"))
    assert len(memory.messages) == 2


def test_add_user_message() -> None:
    memory = ConversationMemory(last_k=2)
    memory.add_user_message("Hello, world!")
    assert len(memory.messages) == 1
    assert isinstance(memory.messages[0], UserMessage)


def test_add_assistant_message() -> None:
    memory = ConversationMemory(last_k=2)
    memory.add_assistant_message("Hello, world!")
    assert len(memory.messages) == 1
    assert isinstance(memory.messages[0], AssistantMessage)


def test_format_messages() -> None:
    memory = ConversationMemory(last_k=2)
    memory.add_user_message("Hello, world!")
    memory.add_assistant_message("Hello, world!")
    memory.add_user_message("How are you?")
    memory.add_assistant_message("I'm fine, thanks")
    messages = memory.format_messages()
    assert len(messages) == 4
    assert messages[0]["content"] == "Hello, world!"
    assert messages[1]["content"] == "Hello, world!"
    assert messages[2]["content"] == "How are you?"
    assert messages[3]["content"] == "I'm fine, thanks"
