from tinylang.llms import ChatOpenAI
from tinylang.tools import Tool
from pydantic import BaseModel
import asyncio


class EvaluateExpressionInput(BaseModel):
    expression: str


def evaluate_expression(expression: str) -> float | str:
    """Evaluate a mathematical expression using python's eval function."""
    try:
        return float(eval(expression))
    except Exception as e:
        return str(e)


chat = ChatOpenAI(
    "gpt-4o",
    tools=[
        Tool(
            name="evaluate_expression",
            description="Evaluate a mathematical expression using python's eval() function and return the result as a float.",
            function=evaluate_expression,
            input_model=EvaluateExpressionInput,
        )
    ],
)

print(chat.invoke("What is 2 to the power of 5 times 2?"))

chat.clear_history()

for chunk in chat.stream_invoke("What is 2 to the power of 5 times 2?"):
    print(chunk, flush=True, end="")


print()
print("Finished first test")
print()

chat.clear_history()


async def main():
    print(await chat.ainvoke("What is 2 to the power of 5 times 2?"))

    chat.clear_history()

    async for chunk in chat.astream_invoke(
        "What is 2 to the power of 5 times (5 modulo 2) times 374?"
    ):
        print(chunk, flush=True, end="")

    print()


asyncio.run(main())
