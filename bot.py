import asyncio
import json
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = "ВАШ_ТОКЕН_БОТА"
WEBAPP_URL = "https://your-domain.com/index.html"
ADMIN_CHAT_ID = 123456789  # Укажите ваш ID в Telegram

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛍️ CHASER SHOP", 
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ]
        ]
    )
    await message.answer(
        "Добро пожаловать в магазин **Chaser Liquids**! 🏆\n"
        "Нажмите кнопку ниже, чтобы открыть каталог:", 
        reply_markup=kb,
        parse_mode="Markdown"
    )

@dp.message(F.web_app_data)
async def handle_order(message: types.Message):
    data = json.loads(message.web_app_data.data)
    items = data.get("items", [])
    total_price = data.get("totalPrice", 0)
    customer = data.get("customer", {})
    
    user = message.from_user
    username_str = f"@{user.username}" if user.username else "нет юзернейма"

    # Формируем список заказанных позиций
    receipt_lines = [f"• **{i['name']}** x{i['quantity']} — {i['sum']} zł" for i in items]
    order_goods = "\n".join(receipt_lines)

    # Ответ покупателю
    user_response = (
        f"✅ **Ваш заказ принят!**\n\n"
        f"📦 **Состав заказа:**\n{order_goods}\n\n"
        f"💰 **Итого:** {total_price} zł\n\n"
        f"Менеджер свяжется с вами для подтверждения!"
    )
    await message.answer(user_response, parse_mode="Markdown")

    # Сообщение администратору (вам)
    admin_notification = (
        f"🔥 **НОВЫЙ ЗАКАЗ!**\n\n"
        f"👤 **Покупатель:** {customer.get('name')}\n"
        f"📞 **Телефон:** `{customer.get('phone')}`\n"
        f"📍 **Доставка:** {customer.get('address') or 'Не указан'}\n"
        f"💬 **Профиль:** {username_str} (ID: `{user.id}`)\n\n"
        f"🛒 **Товары:**\n{order_goods}\n\n"
        f"💰 **Сумма заказа:** **{total_price} zł**"
    )

    try:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID, 
            text=admin_notification, 
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Ошибка отправки уведомления админу: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
