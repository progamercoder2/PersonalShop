from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

from keyboards.reply import start_kb

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