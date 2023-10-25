from pathlib import Path

import numpy as np
import pytest
from PIL import Image as PillowImage

from tinylang.images import Image
from tinylang.memory import ConversationMemory
from tinylang.messages import AssistantMessage, UserMessage

RESOURCES_DIR = (Path(__file__).parent.parent / "resources").resolve()


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


@pytest.fixture(scope="module")
def loaded_image():
    with PillowImage.open(RESOURCES_DIR / "image.png") as img:
        yield np.array(img)


def test_user_message_creation_with_image(loaded_image):
    user_image = Image(loaded_image)
    message_with_image = UserMessage(
        content="Hello with image", prefix="User", image=user_image.to_numpy()
    )
    assert np.array_equal(message_with_image.image, loaded_image)


def test_user_message_to_json_with_image(loaded_image):
    user_image = Image(loaded_image)
    message_with_image = UserMessage(
        content="Hello with image", prefix="User", image=user_image
    )
    json_data = message_with_image.to_json()
    assert "image" in json_data
    assert np.array_equal(json_data["image"], loaded_image)


def test_user_message_copy(loaded_image):
    user_image = Image(loaded_image)
    message_with_image = UserMessage(
        content="Hello with image", prefix="User", image=user_image
    )
    copied_message = message_with_image.copy()
    assert np.array_equal(copied_message.image, loaded_image)
    assert copied_message.prefix == message_with_image.prefix
    assert copied_message.content == message_with_image.content


def test_user_message_str_and_repr(loaded_image):
    user_image = Image(loaded_image)
    message_with_image = UserMessage(
        content="Hello with image", prefix="User", image=user_image
    )
    assert str(message_with_image) == "User: Hello with image"
    assert (
        f"UserMessage(User, Hello with image, tinylang.images.Image object of size: {str(user_image.image_data.shape)})"
        in repr(message_with_image)
    )
