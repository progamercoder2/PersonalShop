from sqlalchemy.orm import Session
from database.base import engine
from database.models import Users, Carts, Categories, FinallyCarts, Orders, Products
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update, select, func, join, DECIMAL, delete

'''создание, чтение,изменение и удаление, данных с помощью функций в базу данных'''


def get_session():
    return Session(engine)


def db_register_user(full_name, chat_id):
    """ регистрация пользователя в базе данных """
    try:
        with get_session() as session:
            query = Users(name=full_name, telegram=chat_id)
            session.add(query)
            session.commit()
        return False
    except IntegrityError:
        return True


def db_update_user(chat_id, phone):
    '''обновление номера телефона пользователя в базе данных'''
    with get_session() as session:
        query = update(Users).where(Users.telegram == chat_id).values(phone=phone)
        session.execute(query)
        session.commit()


def db_create_user_cart(chat_id):
    '''создание корзины пользователя(одна корзина на одного пользователя)'''
    try:
        with get_session() as session:
            subquery = session.scalar(select(Users).where(Users.telegram == chat_id))
            query = Carts(user_id=subquery.id)
            session.add(query)
            session.commit()
            return True
    except IntegrityError:
        return False
    except AttributeError:
        return False


def db_get_all_categories():
    '''получение всех категорий из базы данных'''
    with get_session() as session:
        query = select(Categories)
        return session.scalars(query).all()


def db_get_finally_price(chat_id):
    """Получение итоговой цены"""

    with get_session() as session:
        query = select(func.sum(FinallyCarts.final_price)).select_from(
            join(Carts, FinallyCarts, Carts.id == FinallyCarts.cart_id)).join(Users, Users.id == Carts.user_id).where(
            Users.telegram == chat_id)
        return session.execute(query).fetchone()[0]


def db_get_last_orders(chat_id, limit=5):
    '''получение последних 5 заказов пользователя'''
    with get_session() as session:
        query = (
            select(Orders).
            join(Carts, Orders.cart_id == Carts.id).
            join(Users, Carts.user_id == Users.id).
            where(Users.telegram == chat_id).
            order_by(Orders.id.desc()).
            limit(limit)
        )
        return session.scalars(query).all()


def db_get_product(category_id):
    '''получение продуктов по id категории'''
    with get_session() as session:
        query = select(Products).where(Products.category_id == category_id)
        return session.scalars(query).all()


def db_get_product_by_id(product_id):
    """Получение продукта по id"""
    with get_session() as session:
        query = select(Products).where(Products.id == product_id)
        return session.scalar(query)


def db_get_user_cart(chat_id):
    '''получение корзины пользователя по id корзины'''
    with get_session() as session:
        query = select(Carts).join(Users, Users.id == Carts.user_id).where(Users.telegram == chat_id)
        return session.scalar(query)


def db_add_or_update_item(cart_id: int, product_id: int, product_name: str, product_price: DECIMAL, increment: int = 0):
    """Добавление или обновление товара в корзине"""
    try:
        with get_session() as session:
            item = (
                session.query(FinallyCarts)
                .filter_by(cart_id=cart_id, product_id=product_id)
                .first()
            )

            if item:
                if increment != 0:
                    item.quantity = max(1, item.quantity + increment)
            else:
                qty = 1 if increment <= 0 else increment
                item = FinallyCarts(
                    cart_id=cart_id,
                    product_id=product_id,
                    product_name=product_name,
                    quantity=qty,
                    final_price=0
                )
                session.add(item)

            item.final_price = item.quantity * product_price

            products_sum, total_products = session.query(
                func.coalesce(func.sum(FinallyCarts.final_price), 0),
                func.coalesce(func.sum(FinallyCarts.quantity), 0)
            ).filter(
                FinallyCarts.cart_id == cart_id
            ).one()

            session.query(Carts).filter(
                Carts.id == cart_id
            ).update({
                Carts.total_price: products_sum,
                Carts.total_products: total_products
            })

            session.commit()

            return {
                "status": "ok",
                "total_price": float(products_sum),
                "total_products": int(total_products),
                "product_quantity": item.quantity
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def db_get_product_by_name(product_name):
    """Получение продукта по name"""
    with get_session() as session:
        query = select(Products).where(Products.product_name == product_name)
        return session.scalar(query)


def db_get_cart_items(chat_id: int):
    """возвращает товары из корзины пользователя"""
    with get_session() as session:
        items = (
            session.query(FinallyCarts)
            .join(Carts, FinallyCarts.cart_id == Carts.id)
            .join(Users, Users.id == Carts.user_id)
            .filter(Users.telegram == chat_id)
            .all()
        )
        print("########", items)

        result = []
        for item in items:
            result.append({
                "product_id": item.product_id,
                "product_name": item.product_name,
                "quantity": item.quantity,
                "final_price": float(item.final_price)
            })

        return result


def db_get_user_phone(chat_id):
    '''получение номера телефона пользователя по id'''
    with get_session() as session:
        query = select(Users.phone).where(Users.telegram == chat_id)
        return session.execute(query).scalar()


def db_save_order_history(chat_id):
    '''сохранение истории заказов'''
    cart = db_get_user_cart(chat_id)

    if not cart:
        return None

    with get_session() as session:
        final_items = session.query(FinallyCarts).filter_by(cart_id=cart.id).all()
        for item in final_items:
            session.add(Orders(
                cart_id=cart.id,
                product_name=item.product_name,
                quantity=item.quantity,
                final_price=item.final_price
            ))
        session.commit()


def db_clear_finally_cart(chat_id):
    """Очистка товаров в финальной корзине после оформление покупки"""

    cart = db_get_user_cart(chat_id)

    if not cart:
        return

    with get_session() as session:
        query = delete(FinallyCarts).where(FinallyCarts.cart_id == cart.id)
        session.execute(query)
        session.commit()


def db_get_product_for_delete(chat_id):
    '''удаление товаров из корзины'''
    with get_session() as session:
        query = (
            select(FinallyCarts.id, FinallyCarts.product_name)
            .join(Carts, FinallyCarts.cart_id == Carts.id)
            .join(Users, Carts.user_id == Users.id)
            .where(Users.telegram == chat_id)
        )
        return session.execute(query).fetchall()


def db_increase_product_quantity(finally_cart_id):
    ''''увеличение количества товара в корзине'''
    with get_session() as session:
        item = session.execute(select(FinallyCarts).where(FinallyCarts.cart_id == finally_cart_id)).scalar_one_or_none()
        if not item:
            return False
        product = session.execute(select(Products).where(Products.id == item.product_id)).scalar_one_or_none()
        if not product:
            return False

        item.quantity += 1
        item.final_price = float(product.price) * item.quantity

        session.commit()
        return True


def db_decrease_product_quantity(finally_cart_id):
    '''уменьшение количества товара в корзине'''
    with get_session() as session:
        item = session.execute(select(FinallyCarts).where(FinallyCarts.cart_id == finally_cart_id)).scalar_one_or_none()
        if not item:
            return False
        product = session.execute(select(Products).where(Products.id == item.product_id)).scalar_one_or_none()
        if not product:
            return False
        item.quantity -= 1
        if item.quantity <= 0:
            session.delete(item)
        else:
            item.final_price = float(product.price) * item.quantity
        session.commit()
        return True