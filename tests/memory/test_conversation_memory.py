import pytest  # noqa

from tinylang.memory import ConversationMemory
from tinylang.messages import AssistantMessage, SystemMessage, UserMessage


def test_initialization() -> None:
    cm = ConversationMemory(last_k=4)
    assert len(cm.messages) == 0
    assert cm.last_k == 4


def test_add_message() -> None:
    cm = ConversationMemory(last_k=4)
    cm.add_message(AssistantMessage("Hello"))
    assert len(cm.messages) == 1


def test_add_user_message() -> None:
    cm = ConversationMemory(last_k=4)
    cm.add_user_message("Hi")
    assert isinstance(cm.messages[0], UserMessage)


def test_add_system_message() -> None:
    cm = ConversationMemory(last_k=4)
    cm.add_system_message("System Info")
    assert isinstance(cm.messages[0], SystemMessage)


def test_add_assistant_message() -> None:
    cm = ConversationMemory(last_k=4)
    cm.add_assistant_message("Hello")
    assert isinstance(cm.messages[0], AssistantMessage)


def test_max_len() -> None:
    last_k = 4
    cm = ConversationMemory(last_k=last_k)
    for i in range(20):
        cm.add_user_message(f"Message {i}")
        cm.add_system_message(f"Message AI {i}")
    assert len(cm.messages) == 8


def test_last_k_validation() -> None:
    with pytest.raises(ValueError):
        ConversationMemory(last_k=-1)

    with pytest.raises(ValueError):
        ConversationMemory(last_k=3)
