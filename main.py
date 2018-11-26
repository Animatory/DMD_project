from flask import Flask, request, jsonify, render_template
from queries import *
from functools import wraps

import re
from datetime import datetime, time, timedelta


app = Flask(__name__)


def make_error(code, message):
    err = {
        'status': 'error',
        'data': {
            'code': code,
            'message': message
        }
    }
    return jsonify(err), code


def required_fields(fields):
    def required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if all([f in request.args for f in fields]):
                if 'date' in fields:
                    if not re.match('\d{4}-\d{2}-\d{2}' ,request.args['date']):
                        return make_error(400, 'Date format idi nahui.')
                return f()
            else:
                return make_error(400, ', '.join(list(map(str.capitalize, fields))) + ' are required.')
        return wrap
    return required


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/query1', methods=['GET'])
@required_fields(['username'])
def query1():
    result_db = select1(request.args['username'])
    return jsonify([['car_id', 'number','model_id','vin','color'],result_db])


@app.route('/query2', methods=['GET'])
@required_fields(['date'])
def query2():
    result_db = select2(request.args['date'])
    print(result_db)
    units = {'{:0>2}h-{:0>2}h'.format(hour, hour + 1): result_db[hour] for hour in range(24)}
    return jsonify([['hours', 'count of charging cars'],units])


@app.route('/query3', methods=['GET'])
@required_fields(['start','end'])
def query3():
    result_db = select3(request.args['start'], request.args['end'])
    return jsonify([['Morning','Afternoon','Evening'], result_db])


@app.route('/query4', methods=['GET'])
@required_fields(['username'])
def query4():
    result_db = select4(request.args['username'])
    for row in range(len(result_db)):
        for key in result_db[row]:
            if type(result_db[row][key]) == type(datetime.now()):
                result_db[row][key] = result_db[row][key].strftime("%Y-%m-%d %H:%M:%S")
            if type(result_db[row][key]) is time:
                result_db[row][key] = result_db[row][key].strftime("%H:%M:%S")
    
    return jsonify([['car_id','end_location_id','end_time','payment', 'request_id','route_length','start_location_id','start_time','username','waiting_time'],\
                    result_db])

@app.route('/query5', methods=['GET'])
@required_fields(['date'])
def query5():
    result_db = list(select5(request.args['date']))
    print(result_db)
    for row in range(len(result_db)):
        if type(result_db[row]) is datetime:
            result_db[row] = result_db[row].strftime("%Y-%m-%d %H:%M:%S")
        if type(result_db[row]) is time:
            result_db[row] = result_db[row].strftime("%H:%M:%S")
        if type(result_db[row]) is timedelta:
            result_db[row] = str(result_db[row])
    print(result_db)

    return jsonify([['avg distance km', 'avg duration'],result_db])


@app.route('/query6', methods=['GET'])
def query6():
    result_db = select6()
    return jsonify(result_db)


@app.route('/query7', methods=['GET'])
def query7():
    result_db = select7()
    return jsonify([['car_id','count'],result_db])


@app.route('/query8', methods=['GET'])
@required_fields(['date'])
def query8():
    result_db = select8(request.args['date'])
    return jsonify([['cars_charge_count','username'],result_db])


@app.route('/query9', methods=['GET'])
@required_fields(['period'])
def query9():
    result_db = select4(request.args['period'])
    for row in range(len(result_db)):
        for key in result_db[row]:
            if type(result_db[row][key]) == type(datetime.now()):
                result_db[row][key] = result_db[row][key].strftime("%Y-%m-%d %H:%M:%S")
            if type(result_db[row][key]) is time:
                result_db[row][key] = result_db[row][key].strftime("%H:%M:%S")
    
    return jsonify([[],[result_db]])

@app.route('/query10', methods=['GET'])
def query10():
    result_db = select10()
    for row in range(len(result_db)):
        for key in result_db[row]:
            if type(result_db[row][key]) is datetime:
                result_db[row][key] = result_db[row][key].strftime("%Y-%m-%d %H:%M:%S")
            elif type(result_db[row][key]) is time:
                result_db[row][key] = result_db[row][key].strftime("%H:%M:%S")
            elif type(result_db[row][key]) is timedelta:
                result_db[row][key] = str(result_db[row][key])
            else:
                result_db[row][key] = str(result_db[row][key])
    return jsonify([['car_id','sum_of_average_expenses'],result_db])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)