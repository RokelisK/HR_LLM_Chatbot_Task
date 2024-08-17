import json

from openai.types.chat import ChatCompletionMessageToolCall

from api.external.openai_service.enums import GPTRole
from utils.logger import AppLogger

logger = AppLogger()


def decode_json_string(json_string: str) -> dict | None:
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON string", error=str(e))
        return None


def has_tool_calls(gpt_message) -> bool:
    return bool(gpt_message.tool_calls)


def create_tool_response_message(tool_call, result) -> dict:
    return {
        "role": GPTRole.TOOL,
        "tool_call_id": tool_call.id,
        "content": json.dumps(result),
    }


def build_tool_call_info(tool_call: ChatCompletionMessageToolCall) -> dict:
    return {
        "id": tool_call.id,
        "type": "function",
        "function": tool_call.function.model_dump(),
    }


def create_tool_call_message(tool_call) -> str:
    return json.dumps(
        {
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "arguments": tool_call.function.arguments,
                        "name": tool_call.function.name,
                    },
                }
            ],
        }
    )
