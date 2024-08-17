from enum import StrEnum


class OpenAIModel(StrEnum):
    GPT_4O_2024_08_06 = "gpt-4o-2024-08-06"
    GPT_4O_2024_05_13 = "gpt-4o-2024-05-13"
    GPT_4_TURBO_2024_04_09 = "gpt-4-turbo-2024-04-09"


class GPTRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
