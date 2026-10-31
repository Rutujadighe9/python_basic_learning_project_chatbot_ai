from fastapi import APIRouter

from app.controllers.gemini_ai_controller import gemini_chat
from app.schemas.chat_schema import ChatRequest, ChatResponse

router = APIRouter(prefix="/gemini", tags=["Gemini Chat"])


@router.post("/chat", response_model=ChatResponse)
def chat_with_gemini(request: ChatRequest) -> ChatResponse:
    return gemini_chat(request)