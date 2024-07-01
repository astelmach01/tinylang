from tinylang.llms import ChatOpenAI, ChatClaude
from tinylang.tools import Tool
from pydantic import BaseModel
import asyncio

prompt = "What is the weather in San Francisco in fahrenheit and send an email from doof@aol.com to ukiand@google.com with the subject hello and body hello"
model = "claude-3-5-sonnet-20240620"


def get_weather(location: str, unit: str):
    return f"The weather in {location} is 65 degrees {unit}"


def send_email(to: str, subject: str, body: str):
    return f"Email sent to {to} with subject {subject} and body {body}"


chat = ChatClaude(
    model,
    tools=[
        Tool(
            name="get_weather",
            description="Get the weather in a given location and fahrenheit or celsius",
            function=get_weather,
        ),
        Tool(
            name="send_email",
            description="Send an email to a given recipient with a subject and body",
            function=send_email,
        ),
    ],
    system_message="Use tools always when you can, and use more than 1 at the same time if you need to. Be concise in your responses",
)

print(chat.invoke(prompt))
print("Finished first test")
chat.clear_history()

for chunk in chat.stream_invoke(prompt):
    print(chunk, flush=True, end="")


print()
print("Finished second test")
print()

chat.clear_history()


async def main():
    print(await chat.ainvoke(prompt))
    print("Finished third test")

    chat.clear_history()

    async for chunk in chat.astream_invoke(prompt):
        print(chunk, flush=True, end="")

    print()
    print("Finished fourth test")


asyncio.run(main())
