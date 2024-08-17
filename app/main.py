from fastapi import FastAPI

from api.endpoints.conversation.endpoint import conversation_router
from api.endpoints.messages.endpoint import messages_router

app = FastAPI()
app.include_router(conversation_router, prefix="/api/conversation", tags=["Conversation"])
app.include_router(messages_router, prefix="/api/messages", tags=["Messages"])
