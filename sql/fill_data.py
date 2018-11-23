from postgres import Postgres
from random import randint, choices, choice
from sql.data import *
import string
from sql.config import database_source

db = Postgres(database_source)


def insert_models():
    db.run('DELETE  from model')
    ids = db.all('SELECT provider_id from car_provider')
    script = """INSERT INTO model (class, max_charge, capacity, provider_id, price) VALUES ('{}','{}','{}','{}','{}')"""
    for i in range(10):
        db.run(script.format(rand_item(model_classes),
                             randint(8, 14) * 1000,
                             randint(2, 6),
                             rand_item(ids),
                             choice(range(10, 1000))))


def insert_car_providers():
    db.run('DELETE from car_provider')
    for name in names:
        db.run("""INSERT INTO car_provider (company_name) VALUES ('{}')""".format(name))


def insert_cars():
    db.run('DELETE from car')
    models = db.all('SELECT model_id from model')
    script = """INSERT INTO car (model_id, vin, available, color, number) VALUES ('{}','{}','{}','{}','{}')"""
    for i in range(100):
        rand_number = ''.join(choices(string.ascii_uppercase + string.digits, k=5))
        db.run(script.format(rand_item(models), randint(1e8, 1e9-1), True, rand_item(colors), rand_number))


def insert_location():
    db.run('DELETE from location')
    countries = [''.join(choices(string.ascii_lowercase, k=10)).capitalize() for i in range(10)]
    cities = [''.join(choices(string.ascii_lowercase, k=5)).capitalize() for i in range(100)]
    zipcode = [randint(1e6, 1e7-1) for i in range(100)]
    street = [''.join(choices(string.ascii_lowercase, k=15)).capitalize() for i in range(1000)]
    house = [randint(1, 100) for i in range(100)]
    script = """INSERT INTO location (country, city, zipcode, street, house) VALUES ('{}','{}','{}','{}','{}')"""
    for i in range(1000):
        db.run(script.format(choice(countries), choice(cities), choice(zipcode), choice(street), choice(house)))


if __name__ == '__main__':
    insert_car_providers()
    insert_models()
    insert_cars()
    insert_location()
