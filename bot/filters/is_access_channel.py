import typing
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from bot import config


class IsAccessChannelFilter(BoundFilter):
    key = 'is_access_channel'

    def __init__(self, is_access_channel: bool):
        self.is_access_channel = is_access_channel

    async def check(self, update: typing.Union[types.ChatJoinRequest, types.ChatMemberUpdated]):
        is_access_channel = update.chat.id == config.DONATE_CHANNEL_ID

        if is_access_channel and self.is_access_channel:
            return True
        elif (not is_access_channel) and (not self.is_access_channel):
            return True
        else:
            return False


