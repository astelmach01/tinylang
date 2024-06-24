from tinylang.llms import ChatOpenAI
import asyncio

chat = ChatOpenAI("gpt-4o")

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

    async for chunk in chat.astream_invoke("What is 2 to the power of 5 times (5 modulo 2)?"):
        print(chunk, flush=True, end="")

    print()


asyncio.run(main())
