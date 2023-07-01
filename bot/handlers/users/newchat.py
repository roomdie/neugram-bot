from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


async def newchat_cmd_message_handler(message: types.Message, state: FSMContext):
    await state.reset_data()
    await message.answer("Контекст успешно сброшен.")


async def newchat_reply_message_handler(message: types.Message, state: FSMContext):
    await state.reset_data()
    await message.answer("Контекст успешно сброшен.")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(
        newchat_cmd_message_handler,
        commands="newchat",
        state="*"
    )

    dp.register_message_handler(
        newchat_reply_message_handler,
        text="🧼 Сбросить контекст",
        state="*"
    )


