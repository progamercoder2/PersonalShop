from aiogram.types import Message
from aiogram import Router, F


router = Router()

@router.message(F.contact)
async def update_info_user(message:Message):
    """Обновление, добавление номера телефона"""
    chat_id = message.chat.id
    phone = message.contact.phone_number

    db_update_user(chat_id, phone)


    if db_create_user_cart(chat_id):
        await message.answer("Вы зарегистрированы.")
    await show_main_menu(message)

async def show_main_menu(message: Message):
    pass