from api.endpoints.conversation.models import EvaluateSentimentRequest
from api.external.openai_service.enums import OpenAIModel, GPTRole
from api.external.openai_service.openai_client import OpenAIChat
from helpers.system_descriptions import get_critical_question_description
from services.message_store import MessageStore
from services.sentiment_evaluation.evaluate import evaluate_sentiment_service
from utils.handler_functions import meta

openai_client = OpenAIChat()

questions_dict = {
    1: "Do your current skills allow you to perform your job effectively?",
    2: "How would you assess the challenge level of your current job? Is it too easy, just right, or too difficult according to your expectations?",
    3: "Do you feel motivated to perform your daily tasks? What currently interests you the most in your work?",
    4: "Do you feel that your current position aligns with your professional growth and ambitions? If not, what changes would you like to see?",
    5: "On a scale from 1 to 10, how satisfied are you with your current role?",
}


@meta(
    name="questions_to_ask_the_user",
    description=(
        "This function provides a question for the user to answer."
        "The function should be called iteratively, incrementing the 'number_of_question' parameter with each call. "
        "It will return the next question in the sequence until all questions have been asked. There are a total of 6 questions."
        "On 6th question, this function will evaluate all previous answers from the user, and if needed, will provide an extra critical question."
        "If the critical question won't be needed, the function will return a message that there are no more questions."
    ),
    parameters={
        "type": "object",
        "properties": {
            "number_of_question": {
                "type": "integer",
                "description": (
                    "The sequence number of the question to be asked. Start with 1 for the first question. "
                    "Increment this number by 1 with each subsequent call to ask the next question. "
                    "If the number exceeds the total number of questions, the function may indicate that there are no more questions."
                ),
            },
        },
        "required": ["number_of_question"],
    },
)
async def questions_to_ask_the_user(number_of_question: int) -> str:
    if not number_of_question:
        return "Please provide the 'number_of_question' parameter."

    if number_of_question > 6:
        return "No more questions to ask."

    if number_of_question == 6:
        return await evaluate_user_answers()

    return questions_dict.get(number_of_question, "No more questions to ask.")


async def evaluate_user_answers() -> str:
    conversation_messages = MessageStore().get_user_and_assistant_messages()

    response = await openai_client.generate_response(
        messages=[{"role": GPTRole.SYSTEM, "content": get_critical_question_description()}] + conversation_messages,
        model=OpenAIModel.GPT_4O_2024_08_06,
        response_format=EvaluateSentimentRequest,
    )

    if not response.choices[0].message.parsed.critical_question_is_needed:
        await evaluate_sentiment_service(user_wants_changes=False)
        return "All questions has been answered, thank the user for his participation."

    return "Critical question required! Here is the question: 'Would you like to have major changes of your current job role?'"
