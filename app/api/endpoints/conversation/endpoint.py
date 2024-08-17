from fastapi import APIRouter

from api.endpoints.conversation.controller import generate_answer_service
from api.endpoints.conversation.models import MessageRequest

conversation_router = APIRouter()


@conversation_router.post("/respond")
async def conversation(payload: MessageRequest):
    return await generate_answer_service(payload)
