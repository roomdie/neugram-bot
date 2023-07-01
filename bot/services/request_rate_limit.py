import random
import asyncio
import time
import openai


class RateLimitRetryError(Exception):
    def __init__(self, message):
        self.message = message


# define a retry decorator
def retry_with_exponential_backoff(
        func,
        initial_delay: float = 1,
        exponential_base: float = 2,
        jitter: bool = True,
        max_retries: int = 10,
        errors: tuple = (
                openai.error.InvalidRequestError,
                openai.error.RateLimitError,
                openai.error.Timeout,
                openai.error.ServiceUnavailableError,
        ),
):
    """Retry a function with exponential backoff."""

    async def wrapper(*args, **kwargs):
        # Initialize variables
        num_retries = 0
        delay = initial_delay

        while True:     # Loop until a successful response or max_retries is hit or an exception is raised
            try:
                return await func(*args, **kwargs)

            except errors as e:     # Retry on specific errors
                # Increment retries
                num_retries += 1

                # Check if max retries has been reached
                if num_retries > max_retries:
                    raise RateLimitRetryError(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )

                # Increment the delay
                delay *= exponential_base * (1 + jitter * random.random())

                # Sleep for the delay
                await asyncio.sleep(delay)

            # Raise exceptions for any errors not specified
            except RateLimitRetryError as e:
                raise e

    return wrapper
