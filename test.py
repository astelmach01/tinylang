from tinylang.llms import ChatOpenAI

chat = ChatOpenAI("gpt-4o")

print(chat.invoke("What is 2 + 2?"))
