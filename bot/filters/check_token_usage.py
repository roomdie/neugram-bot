from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher import FSMContext
from bot import models
from bot.services import get_tokens_text


async def check_context_tokens(context: dict, message_tokens: int):
    dialog_context = models.nosql.DialogContext(**context)

    message_num = 1
    while True:
        dialog_message_text = ""

        for dialog_message in dialog_context.messages:
            dialog_message = models.nosql.DialogMessage(**dialog_message)
            dialog_message_text += f"role: {dialog_message.role}" \
                                   f" content: {dialog_message.content}\n"

        dialog_message_tokens = get_tokens_text(dialog_message_text)

        if (dialog_message_tokens + message_tokens) > 8192:
            try:
                dialog_context.messages.remove(
                    dialog_context.messages[message_num % len(dialog_context.messages)]
                )
                message_num += 1
                continue
            except ZeroDivisionError:
                dialog_context.messages.clear()
                return dialog_context
        else:
            return dialog_context


class CheckTokenMessagesFilter(BoundFilter):
    async def check(self, message: types.Message):
        dp: Dispatcher = message.bot.get("dp")
        state: FSMContext = dp.current_state(chat=message.chat.id, user=message.chat.id)
        state_data = await state.get_data()
        context: dict = state_data.get("dialog_context")
        message_tokens = get_tokens_text(message.text)

        if context:
            dialog_context = await check_context_tokens(context, message_tokens)
            await state.update_data(dict(dialog_context=dialog_context.dict()))

        return True
