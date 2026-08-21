import asyncio
import json
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = "ВАШ_ТОКЕН_БОТА"
WEBAPP_URL = "https://your-domain.com/index.html" 

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔥 Магазин и Корзина", 
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ]
        ]
    )
    await message.answer(
        "Добро пожаловать в **Gold Vape Store**!\n"
        "Нажмите кнопку ниже, чтобы открыть каталог и собрать корзину:", 
        reply_markup=kb,
        parse_mode="Markdown"
    )

@dp.message(F.web_app_data)
async def handle_cart_data(message: types.Message):
    # Декодируем входящие данные
    data = json.loads(message.web_app_data.data)
    items = data.get("items", [])
    total_price = data.get("totalPrice", 0)
    
    # Формируем красивый чек
    receipt_lines = []
    for item in items:
        receipt_lines.append(
            f"• **{item['name']}** x{item['quantity']} — {item['sum']} ₽"
        )
    
    order_text = "\n".join(receipt_lines)
    
    response = (
        f"🛒 **Заказ сформирован!**\n\n"
        f"{order_text}\n\n"
        f"💰 **Итого к оплате:** {total_price} ₽\n\n"
        f"Наш менеджер свяжется с вами для подтверждения заказа."
    )
    
    await message.answer(response, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
