import pytest
from pydantic import BaseModel
from tinylang.tools.tool import Tool, process_tools


def sample_function(x: int, y: int = 0) -> int:
    """Sample function for Tool class"""
    return x + y


class SampleInputModel(BaseModel):
    x: int
    y: int = 0


def test_tool_creation():
    tool = Tool(
        name="sample_tool", description="A sample tool", function=sample_function
    )
    assert tool.name == "sample_tool"
    assert tool.description == "A sample tool"
    assert tool.function == sample_function


def test_tool_to_dict():
    tool = Tool(
        name="sample_tool", description="A sample tool", function=sample_function
    )
    tool_dict = tool.to_dict()
    assert tool_dict["type"] == "function"
    assert tool_dict["function"]["name"] == "sample_tool"
    assert tool_dict["function"]["description"] == "A sample tool"
    assert "parameters" in tool_dict["function"]


def test_tool_with_input_model():
    tool = Tool(
        name="sample_tool",
        description="A sample tool",
        function=sample_function,
        input_model=SampleInputModel,
    )
    tool_dict = tool.to_dict()
    assert tool_dict["function"]["parameters"]["properties"]["x"]["type"] == "integer"
    assert tool_dict["function"]["parameters"]["properties"]["y"]["type"] == "integer"
    assert tool_dict["function"]["parameters"]["required"] == ["x"]


def test_process_tools():
    tools = [
        Tool(name="tool1", description="Tool 1", function=lambda x: x),
        Tool(name="tool2", description="Tool 2", function=lambda x, y: x + y),
    ]
    processed_tools = process_tools(tools)
    assert len(processed_tools) == 2
    assert all(tool["type"] == "function" for tool in processed_tools)
    assert processed_tools[0]["function"]["name"] == "tool1"
    assert processed_tools[1]["function"]["name"] == "tool2"


def test_tool_with_complex_input_model():
    class ComplexInputModel(BaseModel):
        name: str
        age: int
        is_student: bool = False
        grades: list[float] = []

    def complex_function(
        name: str, age: int, is_student: bool = False, grades: list[float] = []
    ) -> str:
        return f"Name: {name}, Age: {age}, Student: {is_student}, Grades: {grades}"

    tool = Tool(
        name="complex_tool",
        description="A complex tool",
        function=complex_function,
        input_model=ComplexInputModel,
    )
    tool_dict = tool.to_dict()
    params = tool_dict["function"]["parameters"]
    assert params["properties"]["name"]["type"] == "string"
    assert params["properties"]["age"]["type"] == "integer"
    assert params["properties"]["is_student"]["type"] == "boolean"
    assert params["properties"]["grades"]["type"] == "array"
    assert params["properties"]["grades"]["items"]["type"] == "number"
    assert set(params["required"]) == {"name", "age"}


if __name__ == "__main__":
    pytest.main()
