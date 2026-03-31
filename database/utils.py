from sqlalchemy.orm import Session
from sqlalchemy import update, delete, select, DECIMAL, join, func
from sqlalchemy.exc import IntegrityError

from database.base import engine
from database.models import (Users, Categories, Products, Carts,
                             FinallyCarts, Orders)


def get_session():
    return Session(engine)


def db_register_user(full_name, chat_id):
    """регистрация юзера в дб"""
    try:
        with get_session() as session:
            query = Users(name=full_name, telegram=chat_id)
            session.add(query)
            session.commit()
        return False
    except IntegrityError:
        return True


def db_update_user(chat_id, phone):
    """изменение данных у пользователя, добавление его номера телефона"""
    with get_session() as session:
        query = update(Users).where(Users.telegram == chat_id).values(phone=phone)
        session.execute(query)
        session.commit()


def db_create_user_cart(chat_id):
    """создание корзины юзера"""
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


def db_get_all_category():
    """получение списка категорий"""
    with get_session() as session:
        query = select(Categories)
        return session.scalars(query).all()


def db_get_finally_price(chat_id):
    """Получение итоговой cуммы"""

    with get_session() as session:
        query = select(func.sum(FinallyCarts.final_price)).select_from(
            join(Carts, FinallyCarts, Carts.id == FinallyCarts.cart_id)).join(Users, Users.id == Carts.user_id).where(
            Users.telegram == chat_id)
        return session.execute(query).fetchone()[0]


def db_get_last_orders(chat_id, limit=5):
    """Получение 5 последних заказов пользователя"""

    with get_session() as session:
        query = (
            select(Orders).
            join(Carts, Orders.cart_id == Carts.id).
            join(Users, Users.id == Carts.user_id).
            where(Users.telegram == chat_id).
            order_by(Orders.id.desc()).
            limit(limit)
        )
        return session.scalars(query).all()


def db_get_product(category_id):
    """Получение продукта по id категории"""

    with get_session() as session:
        query = select(Products).where(Products.category_id == category_id)
        return session.scalars(query).all()
