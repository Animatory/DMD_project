from postgres import Postgres
from random import randint, choices
from sql.data import *
import string

db = Postgres('postgres://inno_points:inno_points@localhost:5432/inno_points')


# print(random(0,3))


def insert_models():
    db.run('DELETE  from model')
    ids = db.all('SELECT provider_id from car_provider')
    for i in range(10):
        db.run(
            '''INSERT INTO model (class, max_charge, capacity, provider_id, price) VALUES ('{}',{},{},{},{})'''.format(
                rand_item(model_classes), randint(8, 14) * 1000, randint(2, 6), rand_item(ids),
                                          100 * randint(1000, 2000)))


def insert_car_providers():
    db.run('DELETE from car_provider')
    for name in names:
        db.run('''INSERT INTO car_provider (company_name) VALUES ('{}')'''.format(name))


def insert_cars():
    db.run('DELETE from car')
    models = db.run('SELECT model_id from model')
    for i in range(100):
        rand_number = ''.join(choices(string.ascii_uppercase + string.digits, k=5))
        db.run('''INSERT INTO car (model_id, vin, available, color, number) 
        VALUES ({},{},{},'{}','{}')'''.format(rand_item(models), randint(10000, 99999), 1, rand_item(colors),
                                              rand_number))


if __name__ == '__main__':
    insert_car_providers()
    insert_models()
    insert_cars()
