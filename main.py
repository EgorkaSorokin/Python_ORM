import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import create_tables, Publisher, Book, Sale, Shop, Stock

DSN = 'postgresql://postgres:postgres@localhost:5432/alchemy_db'

engine = sq.create_engine(DSN)

create_tables(engine)

p1 = Publisher(name='Анджей Сапковский', books = [
    Book(title="Меч предназначения"),
    Book(title="Последнее желание"),
    Book(title="Кровь эльфов")])
p2 = Publisher(name='Джордж Мартин', books = [
    Book(title="Игра престолов"),
    Book(title="Битва королей"),
    Book(title="Буря мечей")])
b1 = Book(title="Пир стервятников", publisher=p2)
b2 = Book(title="Танец с драконами", publisher=p2)
b3 = Book(title="Крещение огнём", publisher=p1)

shop1 = Shop(name="Буквоед")
stock1 = Stock(book=b1, shop=shop1, count=50)
sale1 = Sale(price=250, stock=stock1, count=25)
stock2 = Stock(book=b3, shop=shop1, count=50)
sale2 = Sale(price=200, stock=stock2, count=15)

shop2 = Shop(name="Дом книги")
stock3 = Stock(book=b2, shop=shop2, count=50)
sale3 = Sale(price=250, stock=stock3, count=25)
stock4 = Stock(book=b2, shop=shop2, count=50)
sale4 = Sale(price=300, stock=stock4, count=15)

Session = sessionmaker(bind=engine)
s = Session()
s.add_all([p1, p2, b1, b2, b3, shop1, shop2, stock1, stock2, stock3, stock4, sale1, sale2, sale3, sale4])
s.commit()

# x = input()
x = 'Анджей Сапковский'
# print(s.query(Publisher).filter(sq.or_(Publisher.id==x, Publisher.name==x)).all()[0])

p = s.query(Publisher).filter(sq.or_(Publisher.id==x, Publisher.name==x)).all()[0]
sales = s.query(Sale).join(Stock).join(Shop).join(Book).filter(Book.publisher==p).subquery('t')
shops = s.query(Shop).join(Stock).join(Sale).filter(Sale.id==sales.c.id)
for i in shops:
    print(i)

s.close()