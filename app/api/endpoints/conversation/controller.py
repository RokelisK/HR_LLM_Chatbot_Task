from fastapi.responses import JSONResponse

from api.endpoints.conversation.models import MessageRequest
from api.external.openai_service.enums import GPTRole
from services.chatbot.handler import ChatbotHandler


async def generate_answer_service(payload: MessageRequest):
    gpt_response = await ChatbotHandler().handle(payload)

    return JSONResponse(content={"role": GPTRole.ASSISTANT, "content": gpt_response})
