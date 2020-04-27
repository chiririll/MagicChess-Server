import json
from flask import Flask, request
from database import Database
from errors import errors


app = Flask(__name__)
DB = Database('localhost', 'root', 'mysql', 'AutoChess')


# --- Functions --- #
def handle_response(response):
    if type(response) is int:
        print(f'\tError {response}')
        return json.dumps({'error': response, 'description': errors[response]})
    return json.dumps(response)


# --- API --- #
# User
@app.route('/api/check_token')
def check_token():
    return handle_response(DB.check_token(request.args.get('token', 'NULL')))


@app.route('/api/user.add_data')
def user_add_data():
    return 'add data'


@app.route('/api/user.get')
def user_get():
    return request.remote_addr


# Account
@app.route('/api/account.create')
def account_create():
    login = str(request.args.get('login', 'NULL'))
    password = str(request.args.get('password', 'NULL'))
    email = str(request.args.get('email', 'NULL'))
    print(f'creating new user {login}...')
    return handle_response(DB.create_account(login, password, email))


@app.route('/api/account.change_pass')
def account_change_pass():
    return 'token'


@app.route('/api/account.get_token')
def account_get_token():
    return handle_response(DB.get_token(request.args.get('login', 'NULL'), request.args.get('password', 'NULL')))
