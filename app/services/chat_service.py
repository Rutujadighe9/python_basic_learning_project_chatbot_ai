import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from fastapi import HTTPException


def get_llm_reply(message: str) -> str:
    request = Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(
            {
                "model": "llama3.2",
                "messages": [{"role": "user", "content": message}],
                "stream": False,
            }
        ).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            result = json.load(response)
    except HTTPError as error:
        if error.code == 404:
            raise HTTPException(
                status_code=503,
                detail="Ollama model llama3.2 not found. Run: ollama pull llama3.2",
            ) from error
        raise HTTPException(
            status_code=503,
            detail=f"Ollama request failed with status {error.code}.",
        ) from error
    except URLError as error:
        raise HTTPException(
            status_code=503,
            detail="Ollama is not running. Start Ollama and try again.",
        ) from error
    except TimeoutError as error:
        raise HTTPException(
            status_code=504,
            detail="Ollama took too long to respond. Try again.",
        ) from error
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise HTTPException(
            status_code=502,
            detail="Ollama returned an invalid response.",
        ) from error

    message_data = result.get("message")
    if not isinstance(message_data, dict) or not isinstance(
        message_data.get("content"), str
    ):
        raise HTTPException(
            status_code=502,
            detail="Ollama response did not contain a message.",
        )

    return message_data["content"]