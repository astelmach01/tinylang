from typing import Any, Dict, Generator

import pytest
from openai.openai_object import OpenAIObject

from tinylang.chains import Chain  # adjust this import as necessary
from tinylang.llms.base import BaseLLM
from tinylang.memory import ConversationMemory


class MockLLM(BaseLLM):
    def __init__(self) -> None:
        super().__init__(ConversationMemory())

    def load_model(self, model_path: str) -> bool:
        return True

    def chat(self, prompt: str, raw_response: bool = False) -> str | OpenAIObject:
        return "mock response"

    def stream_chat(
        self, prompt: str, raw_response: bool = False
    ) -> Generator[Dict[str, Any], None, None]:
        self.memory.add_user_message(prompt)
        mock_stream_response = iter(
            [
                {"choices": [{"delta": {"content": "Hello, "}}]},
                {"choices": [{"delta": {"content": "World!"}}]},
            ]
        )
        aggregated_content = ""
        for chunk in mock_stream_response:
            content = chunk["choices"][0]["delta"].get("content")
            if not content:
                continue
            aggregated_content += content
            yield chunk if raw_response else content  # type: ignore
        self.memory.add_assistant_message(aggregated_content)


@pytest.fixture
def mock_llm() -> MockLLM:
    return MockLLM()


def test_chain_init(mocker, mock_llm):  # type: ignore
    memory = ConversationMemory()
    prompt = "You are a helpful assistant."
    chain = Chain(llm=mock_llm, memory=memory, prompt=prompt)
    assert chain.llm is mock_llm
    assert chain.memory is memory
    assert len(chain.memory.messages) == 1
    assert chain.memory.messages[0].content == prompt


def test_chain_run(mocker, mock_llm) -> None:  # type: ignore
    chain = Chain(llm=mock_llm)
    mocker.spy(mock_llm, "chat")
    prompt = "What's the weather like?"
    response = chain.run(prompt)
    assert response == "mock response"
    mock_llm.chat.assert_called_once_with(prompt, False)


def test_chain_run_with_raw_response(mocker, mock_llm) -> None:  # type: ignore
    chain = Chain(llm=mock_llm)
    mocker.spy(mock_llm, "chat")
    prompt = "What's the weather like?"
    response = chain.run(prompt, raw_response=True)
    assert response == "mock response"
    mock_llm.chat.assert_called_once_with(prompt, True)


def test_stream_chat(mocker, mock_llm) -> None:  # type: ignore
    mocker.spy(mock_llm.memory, "add_user_message")
    mocker.spy(mock_llm.memory, "add_assistant_message")
    prompt = "Stream this!"
    response_gen = mock_llm.stream_chat(prompt, raw_response=True)
    responses = list(response_gen)
    assert responses == [
        {"choices": [{"delta": {"content": "Hello, "}}]},
        {"choices": [{"delta": {"content": "World!"}}]},
    ]
    mock_llm.memory.add_user_message.assert_called_once_with(prompt)
    mock_llm.memory.add_assistant_message.assert_called_once_with("Hello, World!")
