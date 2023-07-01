import validators
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

import tools.filer
from bot import models
from sqlalchemy import select
from bot.services import get_tokens_text


class CheckTextTokensFilter(BoundFilter):

    async def check(self, message: types.Message):
        text_tokens = get_tokens_text(message.text)

        if text_tokens > 8192:
            if message.chat.type == "private":
                await message.answer(text="Сообщение, которое вы отправили, слишком длинное.")
            else:
                await message.reply(text="Сообщение, которое вы отправили, слишком длинное.")
            return False
        return True
