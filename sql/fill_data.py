from postgres import Postgres
from random import randint, choices
from sql.data import *
import string
from configs import db


def insert_models():
    db.run('DELETE from model')
    ids = db.all('SELECT provider_id from car_provider')
    for i in range(10):
        db.run(
            """INSERT INTO model (class, max_charge, capacity, provider_id, price) VALUES ('{}',{},{},{},{})""".format(
                rand_item(model_classes), randint(8, 14) * 1000, randint(2, 6), rand_item(ids),
                                          100 * randint(1000, 2000)))


def insert_car_providers():
    db.run('DELETE from car_provider')
    for name in names:
        db.run("""INSERT INTO car_provider (company_name) VALUES ('{}')""".format(name))


def insert_cars():
    db.run('DELETE from car')
    models = db.all('SELECT model_id from model')
    for i in range(100):
        rand_number = ''.join(choices(string.ascii_uppercase + string.digits, k=5))
        db.run("""INSERT INTO car (model_id, vin, available, color, number) 
        VALUES ({},{},{},'{}','{}')""".format(rand_item(models), randint(10000, 99999), True, rand_item(colors),
                                              rand_number))


def insert_customers():
    db.run('DELETE from customer')
    for i in range(1000):
        name = rand_item(names)
        username = str(randint(0, 100)) + name + ''.join(choices(string.ascii_uppercase, k=4))
        email = str(randint(0, 1000)) + name + str(randint(0, 1000)) + '@gmail.com'
        db.run('''INSERT INTO customer (username, email, name, surname, phone, location_id) VALUES 
        ('{}','{}','{}','{}','{}',{})'''.format(username,
                                                email,
                                                name,
                                                ''.join(choices(string.ascii_uppercase, k=3)),
                                                '+' + str(randint(1e7, 1e8 - 1)), 1))


#
# def insert_charging_station():
#     db.run('DELETE from charging_station')
#     for i in range(100):
#         db.run("INSERT INTO charging_station (latitude, longitude, available_sockets, maximum_sockets) values ({},{},{},{})".format(ra)
def insert_location():
    db.run('DELETE from location')
    countries = [''.join(choices(string.ascii_lowercase, k=10)).capitalize() for i in range(10)]
    cities = [''.join(choices(string.ascii_lowercase, k=5)).capitalize() for i in range(100)]
    zipcode = [randint(1e6, 1e7 - 1) for i in range(100)]
    street = [''.join(choices(string.ascii_lowercase, k=15)).capitalize() for i in range(1000)]
    house = [randint(1, 100) for i in range(100)]
    for i in range(1000):
        script = """INSERT INTO location (country, city, zipcode, street, house) 
                    VALUES ('{}','{}','{}','{}','{}')"""
        db.run(script.format(choices(countries), choices(cities), choices(zipcode), choices(street), choices(house)))


if __name__ == '__main__':
    insert_car_providers()
    insert_models()
    insert_cars()
    insert_customers()
