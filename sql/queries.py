from sql.fill_data import db

s1 = "SELECT car.car_id,car.number,car.model_id,car.vin,car.color from request inner join car on request.car_id=car.car_id and car.color='red' and car.number like '925%'"


def select1():
    cars = db.all(s1)
    print(cars)


if __name__ == '__main__':
    select1()
