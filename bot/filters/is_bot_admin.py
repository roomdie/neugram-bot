from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
import typing
from bot import config


class IsBotAdminFilter(BoundFilter):
    key = 'is_bot_admin'

    def __init__(self, is_bot_admin: bool):
        self.is_bot_admin = is_bot_admin

    async def check(self, context: typing.Union[types.Message, types.CallbackQuery, types.InlineQuery]):
        user_id = context.from_user.id
        if str(user_id) in config.BOT_ADMINS:
            return self.is_bot_admin and True
        else:
            return False
