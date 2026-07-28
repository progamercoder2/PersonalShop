from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from database.utils import db_get_user_phone

router = Router()


@router.callback_query(F.data=='confirm_order')
async def confirm_order(callback: CallbackQuery, bot: Bot):
    """Оформление заказа"""
    user = callback.from_user
    phone = db_get_user_phone(user.id)

    mention = f'<a href="tg://user?id{user.id}">{user.full_name}</a>'
    user_text = f"новый заказ от {mention}\n Номер телефона покупателя:"
    context = counting_products_from_cart(user.id, user_text)