import asyncio
from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import h01_start, h02_getcontact, h03_order, h04_history, h05_categories, h06_navigation, h10_open_cart, \
    h09_add_to_cart, h08_cart_quantity, h07_product_detail

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(h01_start.router)
dp.include_router(h02_getcontact.router)
dp.include_router(h03_order.router)
dp.include_router(h04_history.router)
dp.include_router(h05_categories.router)
dp.include_router(h06_navigation.router)
dp.include_router(h07_product_detail.router)
dp.include_router(h08_cart_quantity.router)
dp.include_router(h09_add_to_cart.router)
dp.include_router(h10_open_cart.router)
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())