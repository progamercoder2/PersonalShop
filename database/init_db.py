from sqlalchemy.orm import Session
from sqlalchemy import text, select
from database.base import engine, Base
from database.models import Categories, Products, FinallyCarts, Users, Carts
from database.models.orders import Orders


def init_db():
    with engine.connect() as conn:
        # conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS public"))
        conn.commit()

    print("Создаём таблицы...")
    Base.metadata.create_all(engine)

    categories = ("Торты", "Печенье")
    products = (
        ("Торты", "Медовик", 700, "Вкусный", "media/Honeycake.jpg"),
        ("Торты", "Наполеон", 1000, "Вкусный", "media/Napoleon.jpg"),
        ("Торты", "Шоколадный", 900, "Вкусный", "media/Chocolatecake.jpg"),
        ("Печенье", "Шоколадное", 300, "Вкусное", "media/Chocolatecookies.jpg"),
        ("Печенье", "Овсяное", 400, "Вкусное", "media/Oatmealcookies.jpg"),
        ("Печенье", "Банановое", 400, "Вкусное", "media/Bananacookies.jpg"),
    )

    with Session(engine) as session:
        category_map = {}

        for name in categories:
            category = session.scalar(select(Categories).where(Categories.category_name == name))
            if not category:
                category = Categories(category_name=name)
                session.add(category)
                session.flush()
            category_map[name] = category.id

        for category_name, name, price, desc, image in products:
            product_exists = session.scalar(select(Products).where(Products.product_name == name))
            if product_exists:
                continue

            category_id = category_map.get(category_name)
            if category_id:
                product = Products(
                    category_id=category_id,
                    product_name=name,
                    price=price,
                    description=desc,
                    image=image
                )
                session.add(product)

        session.commit()
        print("База успешно инициализирована")


if __name__ == "__main__":
    init_db()
