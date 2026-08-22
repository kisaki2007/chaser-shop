import logging
import os
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    WebAppInfo
)
from aiogram.enums import ParseMode
import asyncio

# Токен вашего бота (или значение из переменной окружения)
TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Ссылка на Netlify с версионированием для сброса кэша Telegram
WEB_APP_URL = "https://timely-syrniki-261609.netlify.app/?v=2.0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Нижняя кнопка меню
    reply_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 Открыть Chaos Shop", web_app=WebAppInfo(url=WEB_APP_URL))]
        ],
        resize_keyboard=True
    )

    # Inline-кнопка в сообщении
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✨ Перейти в магазин", web_app=WebAppInfo(url=WEB_APP_URL))]
        ]
    )

    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        f"Добро пожаловать в **Chaos Shop**! 🖤\n"
        f"Нажмите кнопку ниже, чтобы открыть каталог.",
        reply_markup=inline_kb,
        parse_mode=ParseMode.MARKDOWN
    )

@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    data = json.loads(message.web_app_data.data)
    
    items_text = ""
    for item in data.get("items", []):
        items_text += f"• {item['name']} x{item['qty']} — {item['price'] * item['qty']} PLN\n"
    
    cust = data.get("customer", {})
    order_info = (
        f"🛍 **Новый заказ!**\n\n"
        f"**Состав заказа:**\n{items_text}\n"
        f"**Итого:** {data.get('total')} PLN\n\n"
        f"👤 **Покупатель:** {cust.get('name')}\n"
        f"📞 **Телефон:** {cust.get('phone')}\n"
        f"📍 **Адрес:** {cust.get('address')}"
    )

    await message.answer(f"Спасибо за заказ! 🎉\n\n{order_info}", parse_mode=ParseMode.MARKDOWN)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
