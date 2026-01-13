from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup

def start_kb():
    """start"""
    return ReplyKeyboardMarkup(
        keyboard = [[KeyboardButton(text="Начать👌")]],
        resize_keyboard= True
    )