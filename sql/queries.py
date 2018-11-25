from sql.fill_data import db
from datetime import datetime, timedelta

s1 = "SELECT car.car_id,car.number,car.model_id,car.vin,car.color from request inner join car on request.car_id=car.car_id and car.color='red' and car.number like '925%' and request.username='{}'"
s2 = "SELECT count(charging.car_id) from charging inner join charging_station on charging.station_id = charging_station.station_id and charging.start_date::date = date '{}' and extract(hour from charging.start_date)={}"
s4 = "select * from request where request.username = '{}' and request.start_time >= '{}'"
s5 = "select avg(route_length),avg(start_time-end_time) from request where start_time::date = date '{}'"
s6_1 = "select start_location_id,count(start_location_id) from request  where extract(hour from start_time)<{} and extract(hour from start_time)<{} group by start_location_id order by count(start_location_id)"
s6_2 = "select end_location_id,count(end_location_id) from request where extract(hour from start_time)<{} and extract(hour from start_time)<{} group by end_location_id order by count(end_location_id) "


def select1(username):
    cars = db.all(s1.format(username))
    print(cars)
    return cars


def select2(date):
    mas = []
    for hour in range(24):
        history = db.all(s2.format(date, hour))
        print(str(hour), ':', history[0])
        mas.append(history)
    return mas


def select4(username):
    payments = db.all(s4.format(username, datetime.now() - timedelta(days=31)))
    print(payments)
    return payments


def select5(date):
    stat = db.all(s5.format(date))
    print(stat)
    return stat


def select6():
    result = []
    for start, end in [[7, 10], [12, 14], [17, 19]]:
        top_starts = db.all(s6_1.format(start, end))[-3:]
        top_ends = db.all(s6_2.format(start, end))[-3:]
        print(start, ' top-start locations', end, ' ', top_starts)
        print(start, ' top-end locations', end, ' ', top_ends)
        result.append([top_starts, top_ends])
    return result


if __name__ == '__main__':
    pass
    # select1(None)
    # select2('1970-01-05')
    # select4('11SlavaARDD')
    # select5('2001-09-19')
    # select6()
