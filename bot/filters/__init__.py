from aiogram import Dispatcher
from .check_text_validation import CheckTextTokensFilter
from .check_token_usage import CheckTokenMessagesFilter
from .check_waiting_request import CheckWaitingRequestFilter
from .is_bot_admin import IsBotAdminFilter
from .is_access_channel import IsAccessChannelFilter
from .check_access import CheckAccessFilter


def setup(dp: Dispatcher):
    text_messages = [
        dp.message_handlers,
        dp.edited_message_handlers,
        dp.channel_post_handlers,
        dp.edited_channel_post_handlers,
        dp.callback_query_handlers
    ]

    dp.filters_factory.bind(IsBotAdminFilter, event_handlers=text_messages)
