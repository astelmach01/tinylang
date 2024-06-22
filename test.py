from tinylang.llms import ChatGemini

previous_history = [
    {"role": "user", "content": "Hello, I am Andrew"},
    {"role": "assistant", "content": "Hello Andrew! How can I assist you today?"},
]

openai_chat = ChatGemini(
    "gemini-1.5-flash",
    chat_history=2,
    previous_history=previous_history,
    system_message="You are a helpful assistant.",
)

# First turn (which is actually the second turn considering the previous history)
response1 = openai_chat.invoke("Who am I?")
print(response1)

# Second turn
response2 = openai_chat.invoke("Tell me a joke")
print(response2)

response3 = openai_chat.invoke("What is the capital of France?")
print(response3)

for history in openai_chat.chat_history.get_messages():
    print(history)
