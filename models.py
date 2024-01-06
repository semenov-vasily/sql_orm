import sqlalchemy as sq
import psycopg2
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Таблица издателей
class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), nullable=False, unique=True)

    def __str__(self):
        return self.name

# Таблица книг
class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=50), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    book_publisher = relationship(Publisher, backref="book")

    def __str__(self):
        return f'{self.title}, {self.book_publisher}'

# Таблица магазинов
class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50), nullable=False, unique=True)

    def __str__(self):
        return self.name

# Таблица склада
class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer, nullable=False)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)

    stock_book = relationship(Book, backref="stock")
    stock_shop = relationship(Shop, backref="stock")

    def __str__(self):
        return f'{self.stock_book}, {self.stock_shop}, {self.count}'

# Таблица продаж
class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)

    sale_stock = relationship(Stock, backref="sale")

    def __str__(self):
        return f'{self.sale_stock}, {self.count}, {self.price}, {self.date_sale}'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
