from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.utils import db_get_all_category, db_get_finally_price, db_get_product


def generate_category_menu(chat_id):
    """создание инлайн клавиатуры с категориями продуктов"""
    categories = db_get_all_category()
    total_price = db_get_finally_price(chat_id)

    builder = InlineKeyboardBuilder()
    builder.button(
        text=f'Корзина заказа ({total_price if total_price else 0} рублей)',
        callback_data='Корзина заказа'
    )
    [builder.button(text=category.category_name, callback_data=f'category_{category.id}')
     for category in categories]

    builder.adjust(1, 2)
    return builder.as_markup()


def show_product_by_category(category_id: int):
    """кнопка для показа продуктов по категориям"""
    products = db_get_product(category_id)
    builder = InlineKeyboardBuilder()
    [builder.button(text=product.product_name, callback_data=f'product_view_{product.id}') for product in products]
    builder.adjust(2)
    builder.row(
        InlineKeyboardButton(text="⬅ Назад", callback_data='return_to_category')
    )
    return builder.as_markup()


def quantity_cart_controls(quantity=1):
    """изменение кол-ва товаров в корзине"""
    builder = InlineKeyboardBuilder()
    builder.button(text='➖', callback_data='action -')
    builder.button(text=str(quantity), callback_data='quantity')
    builder.button(text='➕', callback_data='action +')
    builder.button(text='положить в корзину', callback_data='put_in_cart')
    builder.button(text='◀️ Назад', callback_data='from_detail_to_category')
    builder.adjust(3, 1, 1)
    return builder.as_markup(resize_keyboard=True)

def cart_actions_kb():
    '''оформление заказа, добавить и убрать товар'''
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='оформить заказ  ', callback_data='confirm_order'),
        InlineKeyboardButton(text='убрать товар ➖', callback_data='choose_to_remove'),
        InlineKeyboardButton(text='добавить товар ➕', callback_data='choose_to_add'),
    )
    builder.adjust(1, 2)
    return builder.as_markup()
