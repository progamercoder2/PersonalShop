from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from handlers.h03_order import handle_main_menu

router = Router()


@router.message(F.text == "Назад ⬅️")
async def back_to_category_menu(message: Message, bot: Bot):
    """обработка кнопки назад с удалением предыдущего сообщения"""
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except TelegramBadRequest:
        pass

    await handle_main_menu(message, bot)
