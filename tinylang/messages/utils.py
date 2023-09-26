from typing import Dict


def from_json(json: Dict[str, str]):  # type: ignore
    """Return a BaseMessage from a JSON dict."""
    from . import AssistantMessage, SystemMessage, UserMessage

    if json["role"] == "user":
        return UserMessage.from_json(json)
    elif json["role"] == "system":
        return SystemMessage.from_json(json)
    elif json["role"] == "assistant":
        return AssistantMessage.from_json(json)
    else:
        raise ValueError(f"Invalid role: {json['role']}")
