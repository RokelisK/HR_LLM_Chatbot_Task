from api.external.openai_service.openai_client import OpenAIChat
from services.sentiment_evaluation.evaluate import evaluate_sentiment_service
from utils.handler_functions import meta

openai_client = OpenAIChat()


@meta(
    name="final_critical_question_answered",
    description=(
        "This function must be called after the user has answered the critical question, about their job role changes."
        "This function is used to finish the conversation with the user. "
        "In case the user wants to have changes, this function will inform a representative about the user's decision."
        "Otherwise, it will thank the user for his participation."
    ),
    parameters={
        "type": "object",
        "properties": {
            "user_wants_to_have_changes": {
                "type": "boolean",
                "description": "The user's decision about having major changes of their current job role.",
            },
        },
        "required": ["user_wants_to_have_changes"],
    },
)
async def final_critical_question_answered(user_wants_to_have_changes: bool) -> str:
    await evaluate_sentiment_service(user_wants_changes=user_wants_to_have_changes)

    if user_wants_to_have_changes:
        return "Thank you for your feedback. We will inform a representative about your decision."

    return "Thank you for your participation. Have a great day!"
