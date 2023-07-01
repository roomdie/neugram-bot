from aiogram import types, Dispatcher

import tools.filer
from aiogram.dispatcher import FSMContext
from bot import keyboards


async def start_handler(message: types.Message, state: FSMContext):
    start_msg = tools.filer.read_txt("help")

    await message.answer(
        text=start_msg,
        disable_web_page_preview=True,
        reply_markup=keyboards.inline.start.keyboard
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(
        start_handler,
        commands="help",
        state="*"
    )
