from flask import Flask, request, jsonify
from queries import *


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


@app.route('/', methods=['GET'])
def index():
    return 'Hello wold'


@app.route('/query1', methods=['GET'])
def query1():
    if not 'username' in request.args:
        return make_error(400, 'Username field are required')
    
    result_db = select1(request.args.get('username'))
    print(result_db)
    return jsonify(result_db)


@app.route('/query2', methods=['GET'])
def query2():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)