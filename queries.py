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
    cars = db.all(query.format(username), back_as=dict)
    print(cars)
    return cars


def select2(date):
    query = """
        SELECT count(charging.car_id) FROM charging 
        INNER JOIN charging_station 
        ON charging.station_id = charging_station.station_id
        WHERE extract(DAY FROM charging.start_date) = extract(DAY FROM charging.end_date) 
            AND charging.start_date::DATE = DATE '{0}'
            AND '{1}' <= extract(HOUR FROM charging.end_date) 
            AND '{1}' >= extract(HOUR FROM charging.start_date)
        OR extract(DAY FROM charging.start_date) != extract(DAY FROM charging.end_date) 
            AND ('{1}' <= extract(HOUR FROM charging.end_date) 
                AND charging.end_date::DATE = DATE '{0}'
                OR '{1}' >= extract(HOUR FROM charging.start_date) 
                AND charging.start_date::DATE = DATE '{0}')
    """
    data = [db.one(query.format(date, hour), back_as=dict) for hour in range(24)]
    units = ['{:0>2}h-{:0>2}h: {}'.format(hour, hour + 1, data[hour]) for hour in range(24)]
    log = "\n".join(['{:<24}{}'.format(units[i], units[i + 12]) for i in range(12)])
    print(log)
    return data


def select3(start_period='2011-06-24', end_period='2011-08-24'):
    query = """
        SELECT count(request.car_id) FROM request
        WHERE GREATEST(request.start_time::DATE, DATE '{0}') <= LEAST(request.end_time::DATE, DATE '{1}')
        AND ((GREATEST(request.start_time::TIME , TIME '{2:0>2}:00') 
            <= LEAST(request.end_time::TIME, time '{3:0>2}:00'))
            AND request.start_time::DATE = request.end_time::DATE
            OR (request.start_time::TIME <= TIME '{3:0>2}:00' 
                OR request.end_time::TIME >= TIME '{2:0>2}:00')
                AND request.start_time::DATE != request.end_time::DATE)
    """
    count = [db.one(query.format(start_period, end_period, i, j), back_as=dict) for i, j in
             [(7, 10), (12, 14), (17, 19)]]
    log = "{:<10}{:<10}{}\n{:<10}{:<10}{}".format("Morning", "Afternoon", "Evening", *count)
    print(log)
    return count


def select4(username):
    query = """SELECT * FROM request WHERE request.username = '{}' AND request.start_time >= '{}'"""
    payments = db.all(query.format(username, datetime.now() - timedelta(days=31)), back_as=dict)
    print(payments)
    return payments


def select5(date):
    query = "SELECT avg(route_length) FROM request WHERE start_time::DATE = DATE '{}'"
    query2 = "SELECT avg(end_time - start_time) FROM request WHERE start_time::DATE = DATE '{}'"
    stat = db.one(query.format(date))
    stat2 = db.one(query2.format(date))
    return stat, stat2


def select6():
    query = """
        SELECT {0}_location_id, count({0}_location_id) 
        FROM request 
        WHERE ((GREATEST(request.start_time::TIME , '{1:0>2}:00') 
            <= LEAST(request.end_time::TIME, '{2:0>2}:00'))
            AND request.start_time::DATE = request.end_time::DATE
            OR (request.start_time::TIME <= '{2:0>2}:00' 
                OR request.end_time::TIME >= '{1:0>2}:00')
                AND request.start_time::DATE != request.end_time::DATE)
        GROUP BY {0}_location_id
        ORDER BY count({0}_location_id) DESC
        LIMIT 3
    """
    result = []
    for start, end in [[7, 10], [12, 14], [17, 19]]:
        top_starts = db.all(query.format('start', start, end), back_as=dict)
        top_ends = db.all(query.format('end', start, end), back_as=dict)
        result.append(['Most popular pick-up locations on ({}-{}) {}'.format(start, end, top_starts), \
                       'Most popular destination locations on ({}-{}) {}'.format(start, end, top_ends)])
    return result


def select7():
    query = """
        SELECT c.car_id, count(r.request_id)
        FROM request r
        FULL OUTER JOIN car c
        ON r.car_id = c.car_id
        GROUP BY c.car_id ORDER BY count(r.request_id) DESC;
    """
    cars = db.all(query, back_as=dict)
    stoped_cars = cars[len(cars) // 10:]
    print(stoped_cars)
    return stoped_cars


def select8(date):
    query = """
        SELECT r.username, count(c.car_id) AS cars_charge_count 
        FROM request r INNER JOIN charging c 
        ON r.car_id = c.car_id and r.start_time::date = c.start_date ::date and r.start_time>='{}' group by r.username
    """
    res = db.all(query.format(date), back_as=dict)
    print(res)
    return res


def select9(period=30):
    query = """
        SELECT r.workshop_id, s.part_id, SUM(s.amount)
        FROM repair r
        INNER JOIN spent_part s on r.repair_id = s.repair_id
        WHERE current_date - r.end_date <= interval '{}' DAY
        GROUP BY r.workshop_id, part_id ORDER BY SUM(s.amount) desc
    """
    res = db.all(query.format(period), back_as=dict)
    result = {}
    for i in res:
        if i['workshop_id'] in result:
            old = result[i['workshop_id']]
            result[i['workshop_id']] = old if old[1] > i['sum'] else (i['part_id'], i['sum'])
        else:
            result[i['workshop_id']] = (i['part_id'], i['sum'])

    print(result)
    return result


def select10():
    query = '''select r.car_id,c.avg_charge_price + r.avg_repair_price as sum_of_average_expenses
                from (SELECT car_id,avg(price) as avg_repair_price from repair group by car_id order by avg(price)) r
                inner join (
                SELECT car_id,avg(price) as avg_charge_price from charging group by car_id order by avg(car_id)) c
                on c.car_id = r.car_id
                group by r.car_id,c.avg_charge_price + r.avg_repair_price order by c.avg_charge_price + r.avg_repair_price
'''
    cars = db.all(query, back_as=dict)
    cars = cars[-3:]
    print('Top expensive-to-maintain cars:')
    print(cars)
    return cars

if __name__ == '__main__':
    # select1("88JeeDQYI")
    # select2('2033-05-04')
    # select3()
    # select4('11SlavaARDD')
    # select5('2001-09-19')
    # select6()
    # select7()
    # select8('2003-04-25')
    # select9(150)
    select10()
