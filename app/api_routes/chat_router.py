from fastapi import APIRouter

from app.controllers.chat_controller import chat
from app.schemas.chat_schema import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
def chat_with_claude(request: ChatRequest) -> ChatResponse:
    return chat(request)