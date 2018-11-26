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


@app.route('/query1', methods=['POST'])
def query1():
    data = request.get_json()
    if not 'username' in data:
        return make_error(400, 'Username field are required')
    
    result_db = select1(data['username'])
    print(result_db)
    return jsonify(result_db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)