import logging
import os
import json
import asyncio
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

# Токен вашего бота
TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Ссылка на сайт с версионированием ?v=2.1 для сброса кэша
WEB_APP_URL = "https://timely-syrniki-261609.netlify.app/?v=2.1"

# (Опционально) Ваш личный Telegram ID, куда присылать копии заказов
ADMIN_CHAT_ID = None  # Замените на число, например: 123456789

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    reply_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 Открыть Chaos Shop", web_app=WebAppInfo(url=WEB_APP_URL))]
        ],
        resize_keyboard=True
    )

    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✨ Перейти в магазин", web_app=WebAppInfo(url=WEB_APP_URL))]
        ]
    )

    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        f"Добро пожаловать в **Chaos Shop**! 🖤\n"
        f"Нажмите кнопку ниже, чтобы открыть каталог и сделать заказ.",
        reply_markup=inline_kb,
        parse_mode=ParseMode.MARKDOWN
    )

# Прием данных из WebApp формы заказа
@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        
        items = data.get("items", [])
        items_text = ""
        for item in items:
            item_sum = item['price'] * item['qty']
            items_text += f"• **{item['name']}** × {item['qty']} шт. = `{item_sum} PLN`\n"
        
        cust = data.get("customer", {})
        
        order_receipt = (
            f"🛍 **НОВЫЙ ЗАКАЗ!** 😊\n\n"
            f"📦 **Состав заказа:**\n{items_text}\n"
            f"💰 **Итого к оплате:** `{data.get('total')} PLN`\n\n"
            f"👤 **Получатель:** {cust.get('name')}\n"
            f"📞 **Телефон:** `{cust.get('phone')}`\n"
            f"📍 **Адрес:** {cust.get('address')}\n\n"
            f" Telegram покупателя: @{message.from_user.username or 'скрыт'}"
        )

        # 1. Отправляем сообщение покупателю в чат
        await message.answer(
            f"Спасибо за ваш заказ! 😊\n\nВот детали вашей заявки:\n\n{order_receipt}",
            parse_mode=ParseMode.MARKDOWN
        )

        # 2. Если указан ADMIN_CHAT_ID, отправляем копию админу
        if ADMIN_CHAT_ID:
            await bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=f"📥 **Уведомление для администратора:**\n\n{order_receipt}",
                parse_mode=ParseMode.MARKDOWN
            )

    except Exception as e:
        logging.error(f"Ошибка обработки заказа: {e}")
        await message.answer("Произошла ошибка при обработке заказа. Попробуйте снова.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
