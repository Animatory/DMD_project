from postgres import Postgres
from random import randint, choices, choice
from sql.data import *
import string
from config import database_source

db = Postgres(database_source)


def recreate():
    db.run("""drop table request;
              drop table charging;
              drop table repair;
              drop table customer;
              drop table workshop;
              drop table charging_station;
              drop table car;
              drop table model;
              drop table car_provider;
              drop table location;""")
    db.run(open('database-schema.sql', 'r').read())


def insert_models():
    ids = db.all('SELECT provider_id from car_provider')
    script = """INSERT INTO model (class, max_charge, capacity, provider_id, price) VALUES ('{}','{}','{}','{}','{}')"""
    for i in range(10):
        db.run(script.format(choice(model_classes),
                             randint(8, 14) * 1000,
                             randint(2, 6),
                             choice(ids),
                             choice(range(10, 1000))))


def insert_car_providers():
    for name in names:
        db.run("""INSERT INTO car_provider (company_name) VALUES ('{}')""".format(name))


def insert_cars():
    models = db.all('SELECT model_id from model')
    script = """INSERT INTO car (model_id, vin, available, color, number) VALUES ('{}','{}','{}','{}','{}')"""
    for i in range(100):
        rand_number = ''.join(choices(string.ascii_uppercase + string.digits, k=5))
        db.run(script.format(choice(models), randint(1e8, 1e9 - 1), True, choice(colors), rand_number))


def insert_customers():
    script = """INSERT INTO customer (username, email, name, surname, phone, location_id) VALUES 
                ('{}','{}','{}','{}','{}','{}')"""
    for i in range(1000):
        name = choice(names)
        username = str(randint(0, 100)) + name + ''.join(choices(string.ascii_uppercase, k=4))
        email = str(randint(0, 1000)) + name + str(randint(0, 1000)) + '@gmail.com'
        db.run(script.format(username, email, name,
                             ''.join(choices(string.ascii_uppercase, k=3)),
                             '+' + str(randint(1e7, 1e8 - 1)), 1))


def insert_location():
    countries = [''.join(choices(string.ascii_lowercase, k=10)).capitalize() for i in range(10)]
    cities = [''.join(choices(string.ascii_lowercase, k=5)).capitalize() for i in range(100)]
    zipcode = [randint(1e6, 1e7 - 1) for i in range(100)]
    street = [''.join(choices(string.ascii_lowercase, k=15)).capitalize() for i in range(1000)]
    house = [randint(1, 100) for i in range(100)]
    script = """INSERT INTO location (country, city, zipcode, street, house) VALUES ('{}','{}','{}','{}','{}')"""
    for i in range(10000):
        db.run(script.format(*map(choice, [countries, cities, zipcode, street, house])))


def insert_charging_station():
    locations = db.all('SELECT location_id from location')
    script = """INSERT INTO charging_station (available_sockets, maximum_sockets, location_id) 
                VALUES ('{}','{}','{}')"""
    for i in range(1000):
        sockets = randint(5, 10)
        db.run(script.format(sockets, sockets, choice(locations)))


if __name__ == '__main__':
    recreate()
    insert_car_providers()
    insert_models()
    insert_cars()
    insert_location()
    insert_customers()
    insert_charging_station()
