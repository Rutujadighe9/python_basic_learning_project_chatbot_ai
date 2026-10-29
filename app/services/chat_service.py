import os

from anthropic import Anthropic
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()


def get_claude_reply(message: str) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="ANTHROPIC_API_KEY .env file madhe set kara.",
        )

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5"),
        max_tokens=500,
        messages=[{"role": "user", "content": message}],
    )
    return "\n".join(
        block.text for block in response.content if block.type == "text"
    )