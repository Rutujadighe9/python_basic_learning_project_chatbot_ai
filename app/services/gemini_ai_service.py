import logging
import os

from dotenv import load_dotenv
from fastapi import HTTPException
from google import genai
from google.genai.errors import APIError

load_dotenv()
logger = logging.getLogger(__name__)


def get_gemini_reply(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="GEMINI_API_KEY .env file madhe set kara.",
        )

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
            contents=prompt,
        )
    except APIError as error:
        logger.exception("Gemini API request failed")
        raise HTTPException(
            status_code=502,
            detail="Gemini request failed. API key, model, ani quota check kara.",
        ) from error

    if not response.text:
        raise HTTPException(
            status_code=502,
            detail="Gemini kadun empty response milala.",
        )

    return response.text