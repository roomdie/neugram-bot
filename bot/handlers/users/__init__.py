from aiogram import Dispatcher
from . import start
from . import request
from . import newchat


def setup(dp: Dispatcher):
    for module in (start, newchat, request):
        module.register_handlers(dp)
