from api.endpoints.conversation.models import UserEvaluationResult
from api.external.openai_service.enums import GPTRole, OpenAIModel
from api.external.openai_service.openai_client import OpenAIChat
from helpers.system_descriptions import get_user_evaluation_description
from services.message_store import MessageStore
from utils.logger import AppLogger

openai_client = OpenAIChat()
logger = AppLogger()


async def evaluate_sentiment_service(user_wants_changes: bool):
    conversation_messages = MessageStore().get_user_and_assistant_messages()

    response = await openai_client.generate_response(
        messages=[{"role": GPTRole.SYSTEM, "content": get_user_evaluation_description()}] + conversation_messages,
        model=OpenAIModel.GPT_4O_2024_08_06,
        response_format=UserEvaluationResult,
    )

    logger.info("User evaluation response", response=response.choices[0].message.parsed, user_wants_changes=user_wants_changes)
