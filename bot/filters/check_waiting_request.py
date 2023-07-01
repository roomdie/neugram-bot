import validators
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
import tools.filer
from bot import models
from sqlalchemy import select
from datetime import datetime


class CheckWaitingRequestFilter(BoundFilter):
    async def check(self, message: types.Message):
        dp: Dispatcher = message.bot.get("dp")
        state: FSMContext = dp.current_state(chat=message.chat.id, user=message.chat.id)
        state_data = await state.get_data()

        dialog_context_dict: dict = state_data.get("dialog_context")

        if dialog_context_dict:
            dialog_context = models.nosql.DialogContext(**dialog_context_dict)

            result = datetime.now() - datetime.strptime(
                dialog_context.waiting_timeout, '%m/%d/%y %H:%M:%S'
            )
            if result.seconds > 60:
                dialog_context.is_waiting_request = False

            if dialog_context.is_waiting_request:
                msg_text = tools.filer.read_txt("waiting_request")
                if message.chat.type == types.ChatType.PRIVATE:
                    await message.answer(msg_text.format(60-result.seconds))
                else:
                    await message.reply(msg_text.format(60-result.seconds))
                return False
        return True
