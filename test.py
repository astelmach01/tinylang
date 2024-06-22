from tinylang.llms import ChatOpenAI, ChatGemini, ChatClaude
import asyncio
import os

# works
# openai_chat = ChatOpenAI("gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

# print(openai_chat.invoke("Hello"))
# print()

# for chunk in openai_chat.stream_invoke("Hello"):
#     print(chunk, flush=True, end="")
# print()

# gem_chat = ChatGemini("gemini-1.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))

# print(gem_chat.invoke("Hello"))
# for chunk in gem_chat.stream_invoke("Hello"):
#     print(chunk, flush=True, end="")


# claude_chat = ChatClaude(
#     "claude-3-5-sonnet-20240620", api_key=os.getenv("ANTHROPIC_API_KEY")
# )
# print(claude_chat.invoke("Hello"))

# for chunk in claude_chat.stream_invoke("Hello"):
#     print(chunk, flush=True, end="")

# async def main():
#     openai_chat = ChatOpenAI("gpt-4o")
#     gem_chat = ChatGemini("gemini-1.5-flash")
#     claude_chat = ChatClaude("claude-3-5-sonnet-20240620")

#     print(await openai_chat.ainvoke("Hello"))
#     print()
#     async for chunk in openai_chat.astream_invoke("Hello"):
#         print(chunk, flush=True, end="")

#     print()
#     print(await gem_chat.ainvoke("Hello"))
#     async for chunk in gem_chat.astream_invoke("Hello"):
#         print(chunk, flush=True, end="")

#     print()
#     print(await claude_chat.ainvoke("Hello"))
#     async for chunk in claude_chat.astream_invoke("Hello"):
#         print(chunk, flush=True, end="")


# asyncio.run(main())
