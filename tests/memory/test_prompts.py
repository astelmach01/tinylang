import pytest

from tinylang.prompts import Prompt


def test_prompt_formatting() -> None:
    prompt = Prompt("Hello, {name}! How are you?")
    formatted = prompt.format(name="Alice")
    assert formatted == "Hello, Alice! How are you?"

    formatted = prompt.format(name="Bob")
    assert formatted == "Hello, Bob! How are you?"


def test_prompt_formatting_multiple_placeholders() -> None:
    prompt = Prompt("{greeting}, {name}! How are you?")
    formatted = prompt.format(greeting="Hi", name="Alice")
    assert formatted == "Hi, Alice! How are you?"


def test_prompt_formatting_no_placeholders() -> None:
    prompt = Prompt("Hello, world!")
    formatted = prompt.format()
    assert formatted == "Hello, world!"


def test_prompt_with_numbers() -> None:
    prompt = Prompt("Hello, {name}! You are {age} years old.")
    formatted = prompt.format(name="Alice", age=25)
    assert formatted == "Hello, Alice! You are 25 years old."


def test_prompt_formatting_missing_keyword() -> None:
    prompt = Prompt("Hello, {name}! How are you?")
    with pytest.raises(KeyError):
        prompt.format()


def test_prompt_formatting_extra_keyword() -> None:
    prompt = Prompt("Hello, {name}! How are you?")
    # Extra keywords are ignored by str.format
    formatted = prompt.format(name="Alice", age=25)
    assert formatted == "Hello, Alice! How are you?"
