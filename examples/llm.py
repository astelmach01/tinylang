import os

from dotenv import find_dotenv, load_dotenv

from tinylang.llms import OpenAI

load_dotenv(find_dotenv())

openai_api_key = os.environ["OPENAI_API_KEY"]
openai_organization = os.environ["OPENAI_ORGANIZATION"]
model = "gpt-3.5-turbo"

# Regular chatGPT
chatGPT = OpenAI(
    openai_api_key=openai_api_key,
    openai_organization=openai_organization,
    model=model,
)

res = chatGPT.chat("Hello, how are you not streaming?")
print(res)

res = chatGPT.chat("Hello, how are you streaming?", stream=True, raw_response=True)
for chunk in res:
    print(chunk)
