from fill_data import db
from datetime import datetime, timedelta


def select1(username):
    query = """
        SELECT car.car_id, car.number, car.model_id, car.vin, car.color FROM request 
        INNER JOIN car 
        ON request.car_id=car.car_id 
        AND car.color='red' 
        AND car.number LIKE 'AN%' 
        AND request.username='{}'
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


def select3():
    count = db.one("select count(*) from car")
    query = '''select car_id
    from request
    where start_time >= '{}'
      and extract(hour from start_time) >={}
      and extract(hour from end_time) <={}
    group by car_id
    '''
    date = datetime.now() - timedelta(days=7)
    ans = []
    for start, end in [[7, 10], [12, 14], [17, 19]]:
        q = db.all(query.format(date, start, end))
        res = len(q) / count * 100
        print(start, '-', end, ':', res)
        ans.append([[start, end], res])
    return ans


def select4(username):
    s4 = '''select * from request
     where request.username = '{}' and request.start_time >= '{}' '''
    payments = db.all(s4.format(username, datetime.now() - timedelta(days=31)))
    print(payments)
    return payments


def select5(date):
    s5 = '''select avg(route_length),avg(start_time-end_time) 
    from request where start_time::date = date '{}' '''
    stat = db.all(s5.format(date))
    print(stat)
    return stat


def select6():
    s6_1 = '''select start_location_id,count(start_location_id) 
    from request  where extract(hour from start_time)<{} 
    and extract(hour from start_time)<{} group by start_location_id 
    order by count(start_location_id)'''

    s6_2 = '''select end_location_id,count(end_location_id) 
    from request where extract(hour from start_time)<{} 
    and extract(hour from start_time)<{} group by end_location_id 
    order by count(end_location_id) '''

    result = []
    for start, end in [[7, 10], [12, 14], [17, 19]]:
        top_starts = db.all(s6_1.format(start, end))[-3:]
        top_ends = db.all(s6_2.format(start, end))[-3:]
        print(start, ' top-start locations id', end, ' ', top_starts)
        print(start, ' top-end locations id', end, ' ', top_ends)
        result.append([[start, end], top_starts, top_ends])
    return result


def select7():
    s7 = '''select car_id,count(car_id) from request group by car_id order by count(car_id)'''
    least_cars = db.all(s7)
    least_cars = least_cars[:round(len(least_cars) / 10)]
    print(least_cars)
    return least_cars


def select8(date):
    s8 = '''select r.username,count(c.car_id) as cars_charge_count from request r 
    inner join charging c on r.car_id = c.car_id 
    and r.start_time::date = date '{}' 
    and c.start_date::date = date '{}' group by r.username'''
    res = db.all(s8.format(date, date))
    print(res)
    return res


if __name__ == '__main__':
    pass