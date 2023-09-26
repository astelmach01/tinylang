from tinylang.messages import UserMessage

message = UserMessage("Hello, world!")

print(message.to_json())

print(UserMessage.from_json(message.to_json()))
