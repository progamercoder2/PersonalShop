from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database.utils import db_get_product_by_id, db_get_user_cart

router = Router()




@router.callback_query(F.data.startswith('product_view_'))
async def show_product_view_(callback: CallbackQuery, bot: Bot):
    """показ детальной информации о продукте"""
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    await bot.delete_message(chat_id, message_id)

    product_id=int(callback.data.split('_')[-1])
    product=db_get_product_by_id(product_id)
    user_cart= db_get_user_cart(chat_id)
