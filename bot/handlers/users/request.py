import asyncio
import datetime
import html
import logging

from aiogram import types, Dispatcher, exceptions
from aiogram.dispatcher import FSMContext

import tools.filer
from bot.services import request_to_gpt
from bot.services.request_rate_limit import RateLimitRetryError
from bot import models, filters, keyboards


async def request_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    state_data = await state.get_data()

    dots_msg = await message.answer(text="[  .  .  .  ]")
    await message.answer_chat_action(types.ChatActions.TYPING)

    dialog_context_dict: dict = state_data.get("dialog_context")

    if dialog_context_dict:
        dialog_context = models.nosql.DialogContext(**dialog_context_dict)
        new_message = models.nosql.DialogMessage(role="user", content=message.text)
        dialog_context.messages.append(new_message.dict())
    else:
        dialog_context = models.nosql.DialogContext(
            user_id=message.from_user.id, chat_id=message.chat.id
        )
        new_message = models.nosql.DialogMessage(
            role="system", content="You are a helpful assistant."
        )
        dialog_context.messages.append(new_message.dict())
        new_message = models.nosql.DialogMessage(
            role="user", content=message.text
        )
        dialog_context.messages.append(new_message.dict())

    dialog_context.is_waiting_request = True
    dialog_context.waiting_timeout = datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')

    await state.update_data(dict(dialog_context=dialog_context.dict()))
    error_msg = tools.filer.read_txt("error")

    try:
        chatgpt_response_json = await request_to_gpt(dialog_context)
    except RateLimitRetryError as e:
        logging.exception(e)
        return await message.answer(text=error_msg.format(
            error="К сожалению наши сервера перегружены."
                  " Ваш запрос не удалось обработать, попробуйте еще раз.")
        )
    except Exception as e:
        logging.exception(e)
        return await message.reply(text=error_msg.format(error=e))
    finally:
        dialog_context.is_waiting_request = False
        await state.update_data(dict(dialog_context=dialog_context.dict()))

    chatgpt_response = models.nosql.ChatGPTResponse(**chatgpt_response_json)
    chatgpt_response_text = chatgpt_response.choices[0].message.get("content")
    new_message = models.nosql.DialogMessage(
        role="assistant",
        content=chatgpt_response_text
    )
    dialog_context.messages.append(new_message.dict())
    await state.update_data(dict(dialog_context=dialog_context.dict()))
    await dots_msg.delete()

    try:
        if len(chatgpt_response_text) > 4096:
            for x in range(0, len(chatgpt_response_text), 4096):
                await asyncio.sleep(1)
                await message.answer(
                    text=chatgpt_response_text[x:x + 4096], parse_mode="Markdown"
                )
        else:
            await message.answer(
                text=f"{chatgpt_response_text}", parse_mode="Markdown"
            )
    except exceptions.CantParseEntities:
        await message.answer(
            text=f"{html.escape(chatgpt_response_text)}", parse_mode="HTML"
        )
    except Exception as e:
        logging.exception(e)
        return await message.reply(text=error_msg.format(error=e))


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(
        request_handler,
        filters.CheckAccessFilter(),
        filters.CheckTextTokensFilter(),
        filters.CheckTokenMessagesFilter(),
        filters.CheckWaitingRequestFilter(),
        content_types=[types.ContentType.TEXT],
        chat_type=[types.ChatType.PRIVATE, ],
        state="*",
    )
