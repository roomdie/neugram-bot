from aiogram import Dispatcher
from . import errors
from . import users
from . import groups
from . import admins
from . import channels


def setup(dp: Dispatcher):
    for module in (users, channels):
        module.setup(dp)
