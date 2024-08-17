from typing import List

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from api.external.openai_service.enums import OpenAIModel
from helpers.custom_exceptions import OpenAIChatException
from helpers.tenacity_retries import openai_retry_strategy
from utils.env_constants import OPENAI_API_KEY
from utils.logger import AppLogger

logger = AppLogger()
TIMEOUT_SECONDS = 45
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY, timeout=TIMEOUT_SECONDS)


class OpenAIChat:
    @openai_retry_strategy
    async def generate_response(
        self,
        messages: List[dict],
        model: OpenAIModel,
        response_format,
        temperature: float = 0,
        max_tokens: int = 4096,
    ) -> ChatCompletion | None:
        try:
            response = await openai_client.beta.chat.completions.parse(
                messages=messages,
                model=model,
                response_format=response_format,
                timeout=TIMEOUT_SECONDS,
                temperature=temperature,
                max_tokens=max_tokens,
            )

        except Exception as e:
            logger.error("Error in OpenAIChat (generate_response)", messages=messages, model=model, exception=str(e))
            raise OpenAIChatException()

        if not response:
            logger.warning("GPT failed to generate a response (generate_response)", messages=messages, model=model)
            raise OpenAIChatException()

        return response

    @openai_retry_strategy
    async def generate_response_with_tools(
        self,
        messages: List[dict],
        model: OpenAIModel,
        tools: List[dict],
        temperature: float = 0,
        max_tokens: int = 4096,
    ) -> ChatCompletion | None:
        try:
            response = await openai_client.chat.completions.create(
                messages=messages,
                model=model,
                tools=tools,
                tool_choice="auto",
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=TIMEOUT_SECONDS,
            )
        except Exception as e:
            logger.error(
                "Error in OpenAIChat (generate_response_with_tools)", messages=messages, model=model, exception=str(e)
            )
            raise OpenAIChatException()

        if not response:
            logger.warning(
                "GPT failed to generate a response (generate_response_with_tools)", messages=messages, model=model
            )
            raise OpenAIChatException()

        return response
