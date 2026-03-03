from aiogram import Router, F, Bot
from aiogram.types import Message

from database.utils import db_get_last_orders

router = Router()

@router.message(F.text == "📒 История")
async def show_order_history(message: Message):
    """демонстрация 5 последних позиций в заказе"""
    chat_id = message.chat.id
    orders = db_get_last_orders(chat_id)
    if not orders:
        await message.answer("У вас нет заказов⛔")
        return

    text = "Последние 5 заказов\n"
    for item in orders:
        order = item["order"]
        line_price = float(order.final_price)
        text += f"👍{order.product_name} {order.quantity} шт {line_price:.2f} руб"

    await message.answer(text)