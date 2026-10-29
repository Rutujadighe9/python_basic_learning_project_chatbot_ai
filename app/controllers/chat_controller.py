from app.schemas.chat_schema import ChatRequest,ChatResponse
from app.services.chat_service import get_claude_reply


def chat(request:ChatRequest)->ChatResponse :
    reply =get_claude_reply(request.message)
    return ChatResponse(reply=reply)