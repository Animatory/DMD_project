from flask import Flask, request, jsonify
from queries import *
from functools import wraps


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
                return f()
            else:
                return make_error(400, ' '.join(list(map(str.capitalize, fields))) + ' are required.')
        return wrap
    return required


@app.route('/', methods=['GET'])
def index():
    return 'Hello wold'


@app.route('/query1', methods=['GET'])
@required_fields(['username'])
def query1():
    result_db = select1(request.args['username'])
    print(result_db)
    return jsonify(result_db)


@app.route('/query2', methods=['GET'])
@required_fields(['date'])
def query2():
    result_db = select2(request.args['date'])
    return jsonify(result_db)


@app.route('/query3', methods=['GET'])
def query3():
    result_db = select3()
    return result_db


@app.route('/query4', methods=['GET'])
@required_fields(['username'])
def query4():
    result_db = select4(request.args['username'])
    return result_db

@app.route('/query5', methods=['GET'])
@required_fields(['date'])
def query5():
    result_db = select5(request.args['date'])
    return result_db


@app.route('/query6', methods=['GET'])
def query6():
    result_db = select6()
    return result_db


@app.route('/query7', methods=['GET'])
def query7():
    result_db = select7()
    return result_db


@app.route('/query8', methods=['GET'])
@required_fields(['date'])
def query8():
    result_db = select8(request.args['date'])
    return result_db


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)