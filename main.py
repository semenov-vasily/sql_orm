import sqlalchemy
import psycopg2
import json
from datetime import datetime
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = "postgresql://postgres:*****@localhost:5432/sqlalchemy"
engine = sqlalchemy.create_engine(DSN)

# Удаление, создание таблиц
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Заполнение таблиц данными
with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


# Функция запроса данных по проданным книгам заданного издательства
def get_sale(publisher):
    book_all = session.query(Sale).join(Stock).join(Shop).join(Book).join(Publisher)
    if publisher.isdigit():
        book_sale = book_all.filter(Publisher.id == str(publisher)).all()
    else:
        book_sale = book_all.filter(Publisher.name == publisher).all()
    for sale in book_sale:
        print(f'{sale.stock.book.title.ljust(40)} | '
              f'{sale.stock.shop.name.ljust(10)} | '
              f'{str(sale.price).ljust(8)} | '
              f'{datetime.date(sale.date_sale)}')


if __name__ == '__main__':
    publisher = input()
    get_sale(publisher)

    session.close()
