from api.external.openai_service.enums import GPTRole


class MessageStore:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MessageStore, cls).__new__(cls)
            cls._instance.messages = []
        return cls._instance

    def add_system_message(self, system_message: str) -> None:
        if not self.messages:
            self.messages.append({"role": GPTRole.SYSTEM, "content": system_message})

    def add_user_message(self, message: str) -> None:
        self.messages.append({"role": GPTRole.USER, "content": message})

    def add_assistant_message(self, message: str) -> None:
        self.messages.append({"role": GPTRole.ASSISTANT, "content": message})

    def add_tool_request(self, tool_calls: list[dict]) -> None:
        self.messages.append({"role": GPTRole.ASSISTANT, "tool_calls": tool_calls})

    def add_tool_response(self, response: dict) -> None:
        self.messages.append(response)

    def get_all_messages(self) -> list[dict]:
        return self.messages

    def get_user_and_assistant_messages(self) -> list[dict]:
        filtered_messages = [
            message
            for message in self.messages
            if message["role"] in [GPTRole.USER, GPTRole.ASSISTANT] and "tool_calls" not in message
        ]
        return filtered_messages
