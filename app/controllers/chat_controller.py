from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import get_llm_reply


def chat(request: ChatRequest) -> ChatResponse:
    reply = get_llm_reply(request.message)
    return ChatResponse(reply=reply)