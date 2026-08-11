from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

router = Router()

callback_data = 'choose_to_add'
callback_data = 'choose_to_remove'


@router.callback_query(F.data == 'choose_to_add')
async def choose_product_to_add(callback: CallbackQuery):
    """выбор добавленых товаров"""
    pass
