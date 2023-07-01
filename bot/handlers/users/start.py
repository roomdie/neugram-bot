from aiogram import types, Dispatcher

import tools.filer
from aiogram.dispatcher import FSMContext
from bot import keyboards


async def start_handler(message: types.Message, state: FSMContext):
    start_msg = tools.filer.read_txt("start")
    sticker_id = "CAACAgIAAxkBAAMsZKAeZnFYX8mk6xp9KElJX63e7TwAAm8AA9vbfgABmVtQqHuTgHQvBA"
    await message.answer_sticker(
        sticker=sticker_id,
        reply_markup=keyboards.reply.base.keyboard
    )

    await message.answer(
        text=start_msg,
        disable_web_page_preview=True,
        reply_markup=keyboards.inline.access.keyboard
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(
        start_handler,
        commands="start",
        state="*"
    )
