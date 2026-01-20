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