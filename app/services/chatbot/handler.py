import asyncio
import json
import os

from fastapi import HTTPException, status
from openai.types.chat import ChatCompletionMessageToolCall

from api.endpoints.conversation.models import MessageRequest
from api.external.openai_service.enums import OpenAIModel, GPTRole
from api.external.openai_service.openai_client import OpenAIChat
from helpers.gpt import has_tool_calls, build_tool_call_info
from helpers.system_descriptions import get_chatbot_description
from services.message_store import MessageStore
from utils.handler_functions import compile_function_metadata, compile_function_map
from utils.logger import AppLogger

logger = AppLogger()
openai_client = OpenAIChat()

function_meta = compile_function_metadata(os.path.dirname(__file__))
function_map = compile_function_map(os.path.dirname(__file__))

GPT_LOOP_LIMIT = 5


class ChatbotHandler:
    def __init__(self):
        self.message_store = MessageStore()

    async def handle(self, payload: MessageRequest):
        self.message_store.add_system_message(get_chatbot_description(payload.include_personal_information))
        self.message_store.add_user_message(payload.message)

        for _ in range(GPT_LOOP_LIMIT):
            response = await openai_client.generate_response_with_tools(
                messages=self.message_store.get_all_messages(),
                model=OpenAIModel.GPT_4_TURBO_2024_04_09,
                tools=function_meta,
            )

            gpt_message = response.choices[0].message

            if has_tool_calls(gpt_message):
                await ChatbotHandler().process_tool_calls(gpt_message.tool_calls)

            elif gpt_message.content:
                self.message_store.add_assistant_message(gpt_message.content)
                return gpt_message.content

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="GPT did not respond with a message."
        )

    async def process_tool_calls(self, tool_calls: list[ChatCompletionMessageToolCall]):

        aggregated_tool_calls = []
        for tool_call in tool_calls:
            tool_call_info = build_tool_call_info(tool_call)
            aggregated_tool_calls.append(tool_call_info)

        self.message_store.add_tool_request(aggregated_tool_calls)

        tool_call_coroutines = [ChatbotHandler().handle_tool_call(tool_call) for tool_call in tool_calls]
        function_results = await asyncio.gather(*tool_call_coroutines, return_exceptions=True)

        for result in function_results:
            self.message_store.add_tool_response(result)

    @staticmethod
    async def handle_tool_call(tool_call):
        gpt_function_name = tool_call.function.name
        gpt_arguments = json.loads(tool_call.function.arguments)
        function_to_call = function_map.get(gpt_function_name)

        logger.info(
            "Calling a function",
            function_name=gpt_function_name,
            arguments=gpt_arguments,
        )

        try:
            function_response = await function_to_call(**gpt_arguments)
        except Exception as exception:
            logger.error("Function error", function_name=gpt_function_name, error=str(exception))
            return {
                "role": GPTRole.TOOL,
                "tool_call_id": tool_call.id,
                "content": "Function has faced an error.",
            }

        logger.info(
            "Function response",
            function_name=gpt_function_name,
            response=function_response,
        )
        return {
            "role": GPTRole.TOOL,
            "tool_call_id": tool_call.id,
            "content": function_response,
        }
