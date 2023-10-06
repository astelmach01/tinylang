import pytest

from tinylang.llms import OpenAI


@pytest.fixture
def openai_instance() -> OpenAI:
    return OpenAI(
        openai_api_key="your-api-key",
        openai_organization="your-org",
        model="gpt-3.5-turbo",
    )


def test_chat_not_streaming(mocker, openai_instance):  # type: ignore
    mock_response = {"choices": [{"message": {"content": "Hello, World!"}}]}
    mocker.patch("openai.ChatCompletion.create", return_value=mock_response)

    response = openai_instance.chat("Hi there!")
    assert response == "Hello, World!"


def test_chat_streaming(mocker, openai_instance) -> None:  # type: ignore
    mock_stream_response = iter(
        [
            {"choices": [{"delta": {"content": "Hello, "}}]},
            {"choices": [{"delta": {"content": "World!"}}]},
        ]
    )
    mocker.patch("openai.ChatCompletion.create", return_value=mock_stream_response)

    response_gen = openai_instance.stream_chat("Hi there!")
    responses = list(response_gen)
    assert responses == ["Hello, ", "World!"]
