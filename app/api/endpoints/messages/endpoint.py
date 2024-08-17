from fastapi import APIRouter

from api.endpoints.messages.controller import get_current_conversation_messages

messages_router = APIRouter()


@messages_router.get("")
async def messages():
    return await get_current_conversation_messages()
