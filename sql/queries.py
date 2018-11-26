from sql.fill_data import db
from datetime import datetime, timedelta

s4 = "select * from request where request.username = '{}' and request.start_time >= '{}'"
s5 = "select avg(route_length),avg(start_time-end_time) from request where start_time::date = date '{}'"
s6_1 = "select start_location_id,count(start_location_id) from request  where extract(hour from start_time)<{} and extract(hour from start_time)<{} group by start_location_id order by count(start_location_id)"
s6_2 = "select end_location_id,count(end_location_id) from request where extract(hour from start_time)<{} and extract(hour from start_time)<{} group by end_location_id order by count(end_location_id) "
s7 = "select car_id,count(car_id) from request group by car_id order by count(car_id)"


def select1(username):
    query = """
        SELECT car.car_id, car.number, car.model_id, car.vin, car.color FROM request 
        INNER JOIN car 
        ON request.car_id=car.car_id and car.color='red' and car.number like 'AN%' and request.username='{}'
    """
    cars = db.all(query.format(username))
    print(cars)
    return cars


def select2(date):
    query = """
        SELECT count(charging.car_id) FROM charging 
        INNER JOIN charging_station 
        ON charging.station_id = charging_station.station_id
        WHERE extract(DAY FROM charging.start_date) = extract(DAY FROM charging.end_date) 
            AND charging.start_date::date = date '{0}'
            AND '{1}' <= extract(HOUR FROM charging.end_date) 
            AND '{1}' >= extract(HOUR FROM charging.start_date)
        OR extract(DAY FROM charging.start_date) != extract(DAY FROM charging.end_date) 
            AND ('{1}' <= extract(HOUR FROM charging.end_date) 
                AND charging.end_date::date = date '{0}'
                OR '{1}' >= extract(HOUR FROM charging.start_date) 
                AND charging.start_date::date = date '{0}')
    """
    data = [db.all(query.format(date, hour))[0] for hour in range(24)]
    units = ['{:0>2}h-{:0>2}h: {}'.format(hour, hour + 1, data[hour]) for hour in range(24)]
    log = "\n".join(['{:<24}{}'.format(units[i], units[i + 12]) for i in range(12)])
    print(log)
    return data


def select4(username):
    query = 0
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


def select7():
    least_cars = db.all(s7)
    least_cars = least_cars[:round(len(least_cars) / 10)]
    print(least_cars)
    return least_cars


if __name__ == '__main__':
    select1("88JeeDQYI")
    # select2('2033-05-04')
    # select4('11SlavaARDD')
    # select5('2001-09-19')
    # select6()
    # select7()
