import logging
import sys
from pythonjsonlogger import jsonlogger


class AppLogger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AppLogger, cls).__new__(cls)
            cls._instance.logger = logging.getLogger("HR-LLM-Chatbot")
            cls._instance.initialize(*args, **kwargs)
        return cls._instance

    def initialize(self, *args, **kwargs):
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        if not any(isinstance(handler, logging.StreamHandler) for handler in self.logger.handlers):
            stream_handler = logging.StreamHandler(sys.stdout)
            formatter = jsonlogger.JsonFormatter(
                fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
                json_ensure_ascii=False,
            )
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

    def debug(self, message, **kwargs):
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message, **kwargs):
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message, **kwargs):
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message, **kwargs):
        self._log(logging.ERROR, message, **kwargs)

    def critical(self, message, **kwargs):
        self._log(logging.CRITICAL, message, **kwargs)

    def _log(self, level, message, **kwargs):
        try:
            filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}
            self.logger.log(level, message, extra=filtered_kwargs)
        except Exception as e:
            print(f"Error while logging message: {e}")
