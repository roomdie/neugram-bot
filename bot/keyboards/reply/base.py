from aiogram import types


keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn = types.InlineKeyboardButton(
    text="🧼 Сбросить контекст"
)

keyboard.add(btn)
