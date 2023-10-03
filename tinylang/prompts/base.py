from typing import Any


class Prompt:
    def __init__(self, template_str: str) -> None:
        self.template = template_str

    def format(self, **kwargs: Any) -> str:
        return self.template.format(**kwargs)
