from tenacity import retry, stop_after_attempt

TENACITY_RETRIES = 2

openai_retry_strategy = retry(
    stop=stop_after_attempt(TENACITY_RETRIES),
    retry_error_callback=lambda retry_state: None,
)
