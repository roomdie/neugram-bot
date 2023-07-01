from aiogram import Dispatcher
from . import start
from . import request
from . import newchat
from . import help


def setup(dp: Dispatcher):
    for module in (start, newchat, help, request):
        module.register_handlers(dp)
