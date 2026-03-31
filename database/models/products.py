from sqlalchemy import String, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base
from .categories import Categories


class Products(Base):
    __tablename__ = "products" #название класса в базе данных
    id: Mapped[int] = mapped_column(primary_key=True)  #уникальный номер для связи между таблицами, первичный ключ
    product_name: Mapped[str] = mapped_column(String(25), unique=True)  #уникальное название продукта
    description: Mapped[str] #строковое описание
    image: Mapped[str] = mapped_column(String(100)) #строковое значение фотографии для продукта
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2)) #цена. Decimal-число с плавающей точкой precision-целые числа scale-числа после запятой
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id')) #вторичный ключ подключается только к первичному

    product_category: Mapped["Categories"] = relationship(back_populates='products')