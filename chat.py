import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY .env file madhe set kara.")

client = Anthropic(api_key=api_key)

response = client.messages.create(
    model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5"),
    max_tokens=200,
    messages=[
        {
            "role": "user",
            "content": "Node.js ani Python madhla farak 3 lines madhe sang.",
        }
    ],
)

for block in response.content:
    if block.type == "text":
        print(block.text)
