from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from config import MANAGER
from bot_utils.counting_products import counting_products_from_cart
from database.utils import db_get_user_phone, db_save_order_history, db_clean_final_cart

router = Router()


@router.callback_query(F.data == 'confirm_order')
async def confirm_order(callback: CallbackQuery, bot: Bot):
    """Оформление заказа"""
    user = callback.from_user
    phone = db_get_user_phone(user.id)

    mention = f'<a href="tg://user?id{user.id}">{user.full_name}</a>'
    user_text = f"новый заказ от {mention}\n Номер телефона покупателя:"
    context = counting_products_from_cart(user.id, user_text)

    if not context:
        await callback.message.edit_text('Корзина пуста')
        await callback.answer()
        return

    if not MANAGER:
        await callback.message.edit_text('Менеджер не указан')
        await callback.answer()
        return

    count, text, total_price, cart_id = context

    await bot.send_message(MANAGER, text, parse_mode='HTML')

    db_save_order_history(user.id)
    db_clean_final_cart(callback.from_user.id)

    await callback.message.edit_text('Заказ принят. Ожидайте обратной связи от менеджера.')
    await callback.answer('Заказ принят.')