from flask import Flask, escape, request
from database import Database


app = Flask(__name__)
DB = Database('localhost', 'login', 'password', 'AutoChess')


# --- Methods --- #

def verify_token(token):
    if token == 'NULL':
        return False
    if DB.check_token(token):
        return True
    return False

# --------- #

# --- API --- #
# User
@app.route('/api/user.add_data')
def user_add_data():
    if verify_token(request.args.get('token', 'NULL')):
        return 'Valid'
    return 'Invalid'


@app.route('/api/user.get')
def user_get():
    return 'method: user.get'


# Account
@app.route('/api/account.create')
def account_create():
    return 'method: account.create'


@app.route('/api/account.change_pass')
def account_change_pass():
    return 'token'


@app.route('/api/account.get_token')
def account_get_token():
    return 'token'
