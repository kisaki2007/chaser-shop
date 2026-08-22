import asyncio
import json
import logging
import sys

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    WebAppInfo,
)

# ================= КОНФИГУРАЦИЯ =================
BOT_TOKEN = "ТВОЙ_ТОКЕН_БОТА"  # Вставь сюда токен от @BotFather
ADMIN_ID = 123456789  # Вставь сюда свой числовой Telegram ID (узнать в @userinfobot)
WEB_APP_URL = "https://твой-сайт.github.io/"  # Вставь ссылку на твой index.html
ADMIN_USERNAME = "Macwinn"
# ================================================

dp = Dispatcher()


# Обработка команды /start
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛒 Открыть CHAOS SHOP",
                    web_app=WebAppInfo(url=WEB_APP_URL),
                )
            ]
        ]
    )

    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        f"Добро пожаловать в **CHAOS SHOP**.\n"
        f"Нажми на кнопку ниже, чтобы открыть каталог и сделать заказ.",
        reply_markup=kb,
        parse_mode="Markdown",
    )


# Обработка заказа из WebApp
@dp.message(F.web_app_data)
async def web_app_data_handler(message: types.Message, bot: Bot):
    try:
        data = json.loads(message.web_app_data.data)

        user = message.from_user
        username_str = f"@{user.username}" if user.username else "не указан"

        # Формируем список товаров из заказа
        items_list = []
        for item in data.get("items", []):
            item_sum = item["price"] * item["qty"]
            items_list.append(
                f"• **{item['name']}** х {item['qty']} шт. — `{item_sum} PLN`"
            )

        items_text = "\n".join(items_list)
        total_price = data.get("total", 0)

        # Текст уведомления для тебя (администратора)
        admin_message = (
            f"🚀 **НОВЫЙ ЗАКАЗ В CHAOS SHOP!**\n\n"
            f"👤 **Покупатель:** {user.first_name} ({username_str})\n"
            f"🆔 **ID:** `{user.id}`\n\n"
            f"📦 **Состав заказа:**\n{items_text}\n\n"
            f"💰 **Итого к оплате:** `{total_price} PLN`"
        )

        # Текст подтверждения для покупателя
        client_message = (
            f"✅ **Ваш заказ оформлен!**\n\n"
            f"📦 **Ваш выбор:**\n{items_text}\n\n"
            f"💰 **Сумма:** `{total_price} PLN`\n\n"
            f"Для подтверждения и оплаты напишите менеджеру: @{ADMIN_USERNAME}"
        )

        # Отправляем заказ тебе
        await bot.send_message(
            chat_id=ADMIN_ID, text=admin_message, parse_mode="Markdown"
        )

        # Отправляем ответ покупателю
        await message.answer(text=client_message, parse_mode="Markdown")

    except Exception as e:
        logging.error(f"Ошибка при обработке заказа: {e}")
        await message.answer(
            "Произошла ошибка при обработке заказа. Попробуйте ещё раз."
        )


async def main():
    bot = Bot(token=BOT_TOKEN)

    # Настройка кнопки WebApp слева от поля ввода
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="CHAOS SHOP", web_app=WebAppInfo(url=WEB_APP_URL)
        )
    )

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
