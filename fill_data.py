from config import *
from postgres import Postgres
from random import randint, choices, choice
from data import *
import string
from datetime import datetime, time

db = Postgres(
    'postgres://{}:{}@{}:{}/{}'.format(database_user, database_password, database_host, database_port, database))


def recreate():
    db.run("""drop table if exists request;
              drop table if exists charging;
              drop table if exists spent_part;
              drop table if exists repair;
              drop table if exists customer;
              drop table if exists workshop;
              drop table if exists charging_station;
              drop table if exists car;
              drop table if exists model;
              drop table if exists car_part;
              drop table if exists car_provider;
              drop table if exists location;""")
    db.run(open('sql/database-schema.sql', 'r').read())


def insert_fill_tests():
    query1 = """INSERT into customer (username, email, name, surname, phone, location_id) 
                values ('Stipa','stipa@gmail.com','Vasily','Sasniy','+73733773','{}')"""

    query2 = """INSERT INTO car (model_id, vin, available, color, number) values ('{}','{}','{}','{}','{}')"""

    query3 = """INSERT INTO request (username, car_id, payment, start_time, end_time, 
                start_location_id, end_location_id, waiting_time, route_length)
                values ('{}','{}','{}','{}','{}','{}','{}','{}','{}')"""

    locations = db.all('SELECT location_id FROM location')
    try:
        db.run(query1.format(locations[0]))
    except:
        pass  # already exists
    models = db.all('SELECT model_id FROM model')
    for i in range(10):
        db.run(query2.format(models[0], randint(1e6, 1e7 - 1), True, 'red',
                             'AN' + ''.join(choices(string.ascii_lowercase, k=3)).capitalize()))
        last_id = db.one('SELECT MAX(car_id) FROM car')
        db.run(query3.format('Stipa', last_id, 100, '2018-11-07 10:07:07.000000',
                             '2018-11-07 10:07:07.000000', locations[0], locations[1], '00:26:05', 100))


def insert_models():
    ids = db.all('SELECT provider_id FROM car_provider')
    query = """INSERT INTO model (class, max_charge, capacity, provider_id, price) VALUES ('{}','{}','{}','{}','{}')"""
    for i in range(10):
        db.run(query.format(choice(model_classes), randint(8, 14) * 1000, randint(2, 6), choice(ids),
                            choice(range(10, 1000))))


def insert_car_providers():
    for name in names:
        db.run("""INSERT INTO car_provider (company_name) VALUES ('{}')""".format(name))


def insert_cars():
    models = db.all('SELECT model_id FROM model')
    query = """INSERT INTO car (model_id, vin, available, color, number) VALUES ('{}','{}','{}','{}','{}')"""
    for i in range(100):
        rand_number = ''.join(choices(string.ascii_uppercase + string.digits, k=5))
        db.run(query.format(choice(models), randint(1e8, 1e9 - 1), True, choice(colors), rand_number))


def insert_customers():
    query = """INSERT INTO customer (username, email, name, surname, phone, location_id) VALUES 
                ('{}','{}','{}','{}','{}','{}')"""
    for i in range(100):
        name = choice(names)
        username = str(randint(0, 100)) + name + ''.join(choices(string.ascii_uppercase, k=4))
        email = str(randint(0, 1000)) + name + str(randint(0, 1000)) + '@gmail.com'
        db.run(query.format(username, email, name,
                            ''.join(choices(string.ascii_uppercase, k=3)),
                            '+' + str(randint(1e7, 1e8 - 1)), 1))


def insert_location():
    countries = [''.join(choices(string.ascii_lowercase, k=10)).capitalize() for i in range(10)]
    cities = [''.join(choices(string.ascii_lowercase, k=5)).capitalize() for i in range(100)]
    zipcode = [randint(1e6, 1e7 - 1) for i in range(100)]
    street = [''.join(choices(string.ascii_lowercase, k=15)).capitalize() for i in range(1000)]
    house = [randint(1, 100) for i in range(100)]
    query = """INSERT INTO location (country, city, zipcode, street, house) VALUES ('{}','{}','{}','{}','{}')"""
    for i in range(100):
        db.run(query.format(choice(countries), choice(cities), choice(zipcode), choice(street), choice(house)))


def insert_charging_station():
    locations = db.all('SELECT location_id FROM location')
    query = """INSERT INTO charging_station (available_sockets, maximum_sockets, location_id) 
                VALUES ('{}','{}','{}')"""
    for i in range(100):
        sockets = randint(5, 10)
        db.run(query.format(sockets, sockets, choice(locations)))


def insert_workshop():
    locations = db.all('SELECT location_id FROM location')
    query = """INSERT INTO workshop (open_time, close_time, location_id) 
                VALUES ('{}','{}','{}')"""
    for i in range(11):
        start_time = time.isoformat(time(hour=randint(5, 10)))
        end_time = time.isoformat(time(hour=randint(20, 23)))
        db.run(query.format(start_time, end_time, choice(locations)))


def insert_repair():
    cars = db.all('SELECT car_id FROM car')
    workshops = db.all('SELECT workshop_id FROM workshop')
    query = """INSERT INTO repair (car_id, workshop_id, start_date, end_date) 
                VALUES ('{}','{}','{}','{}')"""
    for i in range(11):
        timestamp = randint(start_stamp, end_stamp)
        timedelta = randint(1e5, 1e6)
        start_time = datetime.isoformat(datetime.fromtimestamp(timestamp), sep=' ')
        end_time = datetime.isoformat(datetime.fromtimestamp(timestamp + timedelta), sep=' ')
        db.run(query.format(choice(cars), choice(workshops), start_time, end_time))


def insert_charging():
    cars = db.all('SELECT car_id FROM car')
    stations = db.all('SELECT station_id FROM charging_station')
    query = """INSERT INTO charging (car_id, station_id, start_date, end_date) 
                    VALUES ('{}','{}','{}','{}')"""
    for i in range(100):
        timestamp = randint(start_stamp, end_stamp)
        timedelta = randint(1e3, 2e4)
        start_time = datetime.isoformat(datetime.fromtimestamp(timestamp), sep=' ')
        end_time = datetime.isoformat(datetime.fromtimestamp(timestamp + timedelta), sep=' ')
        db.run(query.format(choice(cars), choice(stations), start_time, end_time))


def insert_request():
    customers = db.all('SELECT username FROM customer')
    cars = db.all('SELECT car_id FROM car')
    locations = db.all('SELECT location_id FROM location')
    query = """INSERT INTO request (username, car_id, payment, start_time, end_time, start_location_id,
                                     end_location_id, waiting_time, route_length) 
                VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')"""
    for i in range(100):
        car_id = choice(cars)
        customer = choice(customers)
        start_locations = choice(locations)
        end_locations = choice(locations)
        length = randint(3, 50)

        waiting_time = randint(300, 1000)
        timestamp = randint(start_stamp, end_stamp)
        duration = round(length / randint(40, 80) * 3600)
        payment = round(duration / 3600 * randint(100, 2000) + waiting_time / 60 * 10)

        waiting_time = list(divmod(waiting_time, 60))
        waiting_time[:1] = divmod(waiting_time[0], 60)
        waiting_time = time.isoformat(time(*waiting_time))

        start_time = datetime.isoformat(datetime.fromtimestamp(timestamp), sep=' ')
        end_time = datetime.isoformat(datetime.fromtimestamp(timestamp + duration), sep=' ')

        db.run(query.format(customer, car_id, payment, start_time, end_time,
                            start_locations, end_locations, waiting_time, length))


def insert_car_parts():
    script = "INSERT INTO car_part (name, price) VALUES ('{}',{})"
    for part in car_parts:
        db.run(script.format(part, randint(100, 20000)))


def insert_spent_parts():
    script = 'INSERT INTO spent_part (repair_id, part_id,amount) VALUES ({},{},{})'
    repairs = db.all('select repair_id from repair')
    parts = db.all('select part_id from car_part')
    for i in range(100):
        db.run(script.format(choice(repairs), choice(parts), randint(1, 5)))


def fill_data():
    recreate()
    insert_location()
    insert_customers()
    insert_car_providers()
    insert_models()
    insert_cars()
    insert_workshop()
    insert_charging_station()
    insert_charging()
    insert_repair()
    insert_request()
    insert_fill_tests()
    insert_car_parts()
    insert_spent_parts()

if __name__ == '__main__':
    fill_data()
