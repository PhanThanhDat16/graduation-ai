"""API routes — single chat endpoint."""

import logging
from fastapi import APIRouter
from src.models import ChatRequest, ChatResponse
from src.agent.chat import chat_with_assistant

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat with the AI assistant. Uses groupId to identify the conversation.

    The assistant fetches conversation context from the backend API,
    processes the message, and posts the response back via the backend API.

    Args:
        request: Chat message with group_id, user_id and user_type

    Returns:
        AI assistant response
    """
    response_text = await chat_with_assistant(
        message=request.message,
        group_id=request.group_id,
        user_id=request.user_id,
        user_type=request.user_type,
    )

    return ChatResponse(
        message=response_text,
        group_id=request.group_id,
        user_type=request.user_type
    )