from services.message_store import MessageStore


async def get_current_conversation_messages():
    return MessageStore().get_user_and_assistant_messages()
