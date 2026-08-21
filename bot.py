import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# Настройки бота
BOT_TOKEN = "ВАШ_BOT_TOKEN"
ADMIN_ID = 123456789  # Укажите ваш Telegram ID
WEB_APP_URL = "https://your-username.github.io/your-repo/"  # Ваша ссылка на index.html

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛒 Открыть Chaser Store", 
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ]
        ]
    )
    await message.answer(
        "Добро пожаловать в Chaser Store! Нажмите кнопку ниже для перехода к каталогу:",
        reply_markup=kb
    )

@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        
        customer = data.get("customer", {})
        items = data.get("items", [])
        total = data.get("total", 0)
        currency = data.get("currency", "PLN")

        items_text = ""
        for item in items:
            items_text += f"• {item['name']} — {item['count']} шт. ({item['price'] * item['count']} {currency})\n"

        order_message = (
            f"🛍 **НОВЫЙ ЗАКАЗ!**\n\n"
            f"👤 **Покупатель:** {customer.get('name')}\n"
            f"📞 **Телефон:** {customer.get('phone')}\n"
            f"📍 **Адрес / Доставка:** {customer.get('address')}\n"
            f"💬 **Профиль:** @{message.from_user.username or 'нет_юзернейма'} (ID: `{message.from_user.id}`)\n\n"
            f"📦 **Товары:**\n{items_text}\n"
            f"💰 **Итого к оплате:** `{total} {currency}`"
        )

        # Сообщение клиенту
        await message.answer("✅ Ваш заказ успешно оформлен! Мы свяжемся с вами в ближайшее время.")

        # Уведомление администратору
        await bot.send_message(chat_id=ADMIN_ID, text=order_message, parse_mode="Markdown")

    except Exception as e:
        logging.error(f"Ошибка при обработке заказа: {e}")
        await message.answer("Произошла ошибка при отправке заказа. Попробуйте еще раз.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
