from typing import List, Dict, Any, Callable, Optional, Type, Union
from pydantic import BaseModel, create_model
from pydantic.json_schema import model_json_schema
import inspect


class Tool:
    def __init__(
        self,
        name: str,
        description: str,
        function: Union[Callable, Callable[..., Any]],
        input_model: Optional[Type[BaseModel]] = None,
    ):
        self.name = name
        self.description = description
        self.function = function
        self.input_model = input_model or self._create_input_model()
        self.is_async = inspect.iscoroutinefunction(function)

    def to_dict(self) -> Dict[str, Any]:
        schema = model_json_schema(self.input_model)
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": schema,
            },
        }

    def _create_input_model(self) -> Type[BaseModel]:
        annotations = self.function.__annotations__
        fields = {
            name: (annotation, ...)  # ... means the field is required
            for name, annotation in annotations.items()
            if name != "return"
        }
        return create_model(f"{self.name}Input", **fields)


def process_tools(tools: List[Tool]) -> List[Dict[str, Any]]:
    return [tool.to_dict() for tool in tools]
