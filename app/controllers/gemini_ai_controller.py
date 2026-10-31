from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.gemini_ai_service import get_gemini_reply


def gemini_chat(request: ChatRequest) -> ChatResponse:
    reply = get_gemini_reply(request.message)
    return ChatResponse(reply=reply)