from postgres import Postgres
from random import randint, choices, choice
from data import *
import string
from config import database_source
from datetime import datetime, time, timedelta as td

db = Postgres(database_host)


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
    for i in range(100):
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
    for i in range(100):
        db.run(script.format(choice(countries), choice(cities), choice(zipcode), choice(street), choice(house)))


def insert_charging_station():
    locations = db.all('SELECT location_id from location')
    script = """INSERT INTO charging_station (available_sockets, maximum_sockets, location_id) 
                VALUES ('{}','{}','{}')"""
    for i in range(100):
        sockets = randint(5, 10)
        db.run(script.format(sockets, sockets, choice(locations)))


def insert_workshop():
    locations = db.all('SELECT location_id from location')
    script = """INSERT INTO workshop (open_time, close_time, location_id) 
                VALUES ('{}','{}','{}')"""
    for i in range(11):
        start_time = time.isoformat(time(hour=randint(5, 10)))
        end_time = time.isoformat(time(hour=randint(20, 23)))
        db.run(script.format(start_time, end_time, choice(locations)))


def insert_repair():
    cars = db.all('SELECT car_id from car')
    workshops = db.all('SELECT workshop_id from workshop')
    script = """INSERT INTO charging (car_id, station_id, start_date, end_date) 
                VALUES ('{}','{}','{}','{}')"""
    for i in range(11):
        timestamp = randint(start_stamp, end_stamp)
        timedelta = randint(1e5, 1e6)
        start_time = datetime.isoformat(datetime.fromtimestamp(timestamp), sep=' ')
        end_time = datetime.isoformat(datetime.fromtimestamp(timestamp + timedelta), sep=' ')
        db.run(script.format(choice(cars), choice(workshops), start_time, end_time))


def insert_charging():
    cars = db.all('SELECT car_id from car')
    stations = db.all('SELECT station_id from charging_station')
    script = """INSERT INTO charging (car_id, station_id, start_date, end_date) 
                    VALUES ('{}','{}','{}','{}')"""
    for i in range(1100):
        timestamp = randint(2e1, 2e6)
        timedelta = randint(1e2, 1e3)
        start_time = datetime.isoformat(datetime.fromtimestamp(timestamp), sep=' ')
        end_time = datetime.isoformat(datetime.fromtimestamp(timestamp + timedelta), sep=' ')
        db.run(script.format(choice(cars), choice(stations), start_time, end_time))


def insert_request():
    customers = db.all('SELECT username from customer')
    cars = db.all('SELECT car_id from car')
    locations = db.all('SELECT location_id from location')
    script = """INSERT INTO request (username, car_id, payment, start_time, end_time, start_location_id,
                                     end_location_id, waiting_time, route_length) 
                VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')"""
    for i in range(1000):
        car_id = choice(cars)
        customer = choice(customers)
        start_locations = choice(locations)
        end_locations = choice(locations)
        length = randint(3, 50)

        waiting_time = randint(300, 3000)
        timestamp = randint(start_stamp, end_stamp)
        duration = round(length / randint(40, 120) * 3600)
        payment = round(duration / 3600 * randint(100, 2000) + waiting_time / 60 * 10)

        waiting_time = list(divmod(waiting_time, 60))
        waiting_time[:1] = divmod(waiting_time[0], 60)
        waiting_time = time.isoformat(time(*waiting_time))

        start_time = datetime.isoformat(datetime.fromtimestamp(timestamp), sep=' ')
        end_time = datetime.isoformat(datetime.fromtimestamp(timestamp + duration), sep=' ')

        db.run(script.format(customer, car_id, payment, start_time, end_time,
                             start_locations, end_locations, waiting_time, length))


def fill_data():
    pass
    # recreate()
    # insert_location()
    # insert_customers()
    # insert_car_providers()
    # insert_models()
    # insert_cars()
    # insert_charging_station()
    # insert_charging()
    # insert_workshop()
    # insert_repair()
    # insert_request()


# insert_charging()

if __name__ == '__main__':
    fill_data()
