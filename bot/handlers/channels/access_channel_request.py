from aiogram import types, Dispatcher
import tools.filer
from bot import filters


async def channel_handler(chat_member: types.ChatMemberUpdated):
    if chat_member.new_chat_member.is_chat_member():
        access_successful_msg = tools.filer.read_txt("access_successful")

        await chat_member.bot.send_message(
            chat_id=chat_member.new_chat_member.user.id,
            text=access_successful_msg,
            disable_web_page_preview=True
        )


async def channel_join_request_handler(chat_join_request: types.ChatJoinRequest):
    keyboard = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(
        text="Перейти",
        url="https://t.me/donate"
    )
    keyboard.add(btn)
    request_msg = tools.filer.read_txt("request_to_access")
    await chat_join_request.bot.send_message(
        chat_id=chat_join_request.from_user.id,
        text=request_msg,
        disable_web_page_preview=True,
        reply_markup=keyboard
    )


def register_handlers(dp: Dispatcher):
    dp.register_chat_member_handler(
        channel_handler,
        filters.IsAccessChannelFilter(True),
        state="*"
    )

    dp.register_chat_join_request_handler(
        channel_join_request_handler,
        filters.IsAccessChannelFilter(True),
        state="*"
    )
