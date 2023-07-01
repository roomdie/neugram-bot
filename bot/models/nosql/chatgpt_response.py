import typing
from pydantic import BaseModel


class Choice(BaseModel):
    finish_reason: str = None
    index: int = 0
    logprobs: None = None
    message: dict = dict()


class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class ChatGPTResponse(BaseModel):
    choices: typing.List[Choice]
    created: int
    id: str
    model: str
    object: str
    usage: Usage
