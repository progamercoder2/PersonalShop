from aiogram import Router, F, Bot
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
