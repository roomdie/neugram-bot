from aiogram import types

keyboard = types.InlineKeyboardMarkup()

btn = types.InlineKeyboardButton(
    text="Оформить доступ",
    url="https://t.me/+e2DhFeZo7axkYzFi"    # here paste your private link from @donate
)

keyboard.add(btn)
