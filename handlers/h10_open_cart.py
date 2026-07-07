from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery

router = Router()


@router.message(F.text == "🛒 Корзина")
async def handle_cart(message: Message):
    """демонстрация 1:корзины с помощью reply кнопок"""
    await show_cart(chat_id = message.chat.id, send_fn = message.answer)

@router.callback_query(F.data == "Корзина заказа")
async def open_cart(callback: CallbackQuery):
    """Демонстрация 2: корзины с помощью inline кнопок"""
    await show_cart(chat_id=callback.from_user.id, send_fn=callback.message.answer)
    await callback.answer()

async def show_cart(chat_id, send_fn):
    cart_items=db_get_cart_items(chat_id)
    if not cart_items:
        await send_fn('корзина пуста')
        return


    text= 'содержимое корзины\n'
    total = 0
    for item in cart_items:
        total=float(item['final_price'])+total
        text+=f'{item['product_name']} {item['quantity']} шт. {item['final_price']} руб. \n'
        text+=f'\nИтог:{total:.2f} руб.'
        await send_fn(text, reply_markup=cart_action_kb())