from tinylang.llms import ChatOpenAI, ChatClaude
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


chat = ChatClaude(
    "claude-3-5-sonnet-20240620",
    tools=[
        Tool(
            name="evaluate_expression",
            description="Evaluate a mathematical expression using python's eval() function and return the result as a float.",
            function=evaluate_expression,
            input_model=EvaluateExpressionInput,
        )
    ],
    system_message="Use tools always when you can, and use more than 1 at the same time if you need to",
)

# print(chat.invoke("What is 2 to the power of 5 times (27 modulo 14) times 374?"))
# print("Finished first test")
# chat.clear_history()

for chunk in chat.stream_invoke(
    "What is 2 to the power of 5 times (27 modulo 14) times 374,462?"
):
    print(chunk, flush=True, end="")


print()
print("Finished second test")
print()

chat.clear_history()


async def main():
    print(await chat.ainvoke("What is 2 to the power of 5 times 2?"))
    print("Finished third test")

    chat.clear_history()

    async for chunk in chat.astream_invoke(
        "What is 2 to the power of 5 times (5 modulo 2) times 374?"
    ):
        print(chunk, flush=True, end="")

    print()
    print("Finished fourth test")


asyncio.run(main())
