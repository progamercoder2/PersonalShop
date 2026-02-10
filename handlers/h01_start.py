from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from database.utils import db_register_user
from handlers.h02_getcontact import show_main_menu
from keyboards.reply import start_kb, phone_button

router = Router()


@router.message(CommandStart())
async def command_start(message: Message):
    """происходит приветствие с отправкой фото"""
    photo = FSInputFile("media/welcome.jpg")
    await message.answer_photo(
        photo=photo,
        caption=f"Добрый день, <i>{message.from_user.full_name}</i>\nНажмите кнопку ниже, чтобы начать",
        parse_mode='HTML',
        reply_markup=start_kb()
    )


@router.message(F.text == "Начать👌")
async def start_button(message: Message):
    await handle_start(message)


async def handle_start(message: Message):
    await register_user(message)


async def register_user(message: Message):
    """регистрация пользователя"""
    chat_id = message.chat.id
    full_name = message.from_user.full_name

    if db_register_user(full_name, chat_id):
        await message.answer(text="Добро пожаловать!😊")
        await show_main_menu(message)
    else:
        await message.answer(text="Предоставьте ваш номер телефона📞", reply_markup=phone_button())
