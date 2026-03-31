from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base

class Users(Base):
    __tablename__ = "users" #название класса в базе данных
    id: Mapped[int] = mapped_column(primary_key=True) #уникальный номер для связи между таблицами
    name: Mapped[str] = mapped_column(String(70)) #имя пользователя (mapped_column уточняет как именно записано в таблице)
    telegram: Mapped[int] = mapped_column(BigInteger, unique=True) #уникальный номер в телеграме BigInterger позволяет писать много символов unique=true -уникальное число
    phone: Mapped[str] = mapped_column(String, nullable=True) #строковый номер телефона.  nullable=true позволяет его не заполнять данные в таблицу
    language: Mapped[str] = mapped_column(String(10), default="ru") #поле отвечающий за параметр выбора языка

    carts: Mapped[int] = relationship("Carts", back_populates='user_cart') #поле указывает на класс с которым установлена связь. Более детально на него указывает параметр back_populates

    def __str__(self):
        return self.name