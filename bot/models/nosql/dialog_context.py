from pydantic import BaseModel
import typing
from datetime import datetime


class DialogMessage(BaseModel):
    role: str = None
    content: str = None


class DialogContext(BaseModel):
    messages: typing.List[dict] = list()
    user_id: int = None
    chat_id: int = None
    is_waiting_request: bool = False
    waiting_timeout: str = datetime.now().strftime('%m/%d/%y %H:%M:%S')

    class Config:
        arbitrary_types_allowed = True

