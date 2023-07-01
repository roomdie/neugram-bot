from aiogram import Dispatcher
from . import access_channel_request


def setup(dp: Dispatcher):
    for module in (access_channel_request,):
        module.register_handlers(dp)
