from typing import List, Dict, Any, Callable, Optional, Type
from pydantic import BaseModel, create_model
from pydantic.json_schema import model_json_schema


class Tool:
    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        input_model: Optional[Type[BaseModel]] = None,
    ):
        self.name = name
        self.description = description
        self.function = function
        self.input_model = input_model or self._create_input_model()

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
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": (
                    tool.input_model.model_json_schema() if tool.input_model else {}
                ),
            },
        }
        for tool in tools
    ]


def get_default_tools() -> List[Tool]:
    class EvaluateExpressionInput(BaseModel):
        expression: str

    def evaluate_expression(expression: str) -> float | str:
        """Evaluate a mathematical expression using python's eval function."""
        try:
            return float(eval(expression))
        except Exception as e:
            return str(e)

    return [
        Tool(
            name="evaluate_expression",
            description="Evaluate a mathematical expression using python's eval() function and return the result as a float.",
            function=evaluate_expression,
            input_model=EvaluateExpressionInput,
        )
    ]
