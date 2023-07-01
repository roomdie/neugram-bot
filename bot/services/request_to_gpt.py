import asyncio
import random

import openai
from bot.models.nosql import DialogContext
from bot import config
from .request_rate_limit import retry_with_exponential_backoff, RateLimitRetryError


@retry_with_exponential_backoff
async def request_to_gpt(dialog_context: DialogContext):
    openai.api_key = random.choice(config.API_KEYS)
    try:
        chatgpt_response_json = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo-16k",
                messages=dialog_context.messages,
                max_tokens=8192,
                temperature=0.7,
                top_p=1,
                presence_penalty=0,
                frequency_penalty=0,
            )
    except Exception as e:
        raise e

    return chatgpt_response_json

