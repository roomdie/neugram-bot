from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
import tools.filer
from bot import config, keyboards


class CheckAccessFilter(BoundFilter):
    async def check(self, message: types.Message):
        user_id = message.from_user.id
        access_channel_member = await message.bot.get_chat_member(
            chat_id=config.DONATE_CHANNEL_ID,
            user_id=user_id
        )

        if access_channel_member.is_chat_member():
            return True
        else:
            has_no_access_msg = tools.filer.read_txt("has_no_access")
            await message.answer(
                text=has_no_access_msg,
                disable_web_page_preview=True,
                reply_markup=keyboards.inline.access.keyboard
            )
            return False
