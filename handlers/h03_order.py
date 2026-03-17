from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from handlers.h02_getcontact import show_main_menu
from keyboards.inline import generate_category_menu
from keyboards.reply import back_to_main_menu

router = Router()


@router.message(F.text == "✅ Сделать заказ")
async def make_order(message: Message, bot):
    """обработка кнопки сделать заказ и выбор категории товаров"""
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text="Формирование заказа", reply_markup=back_to_main_menu())
    await message.answer(text="Выберите категорию", reply_markup=generate_category_menu(chat_id))

@router.message(F.text == "Главное меню")
async def handle_main_menu(message: Message, bot:Bot):
    """переход в главное меню с удалением прошлых действий"""
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except TelegramBadRequest:
        pass
    await show_main_menu(message)