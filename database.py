import pymysql
import hashlib
import random
import time
import re


class Database:

    lifetime = 3600

    def __init__(self, ip, user, password, db):
        self.ip = ip
        self.user = user
        self.password = password
        self.db = db
        self.__checkDB__()

    def __connect__(self):
        return pymysql.connect(self.ip, self.user, self.password, self.db)

    def __checkDB__(self):
        print('Checking tables in database ' + self.db)
        tables = {
            'accounts': 'CREATE TABLE accounts (id INT(11) AUTO_INCREMENT UNIQUE, login VARCHAR(20) NOT NULL UNIQUE, \
            password VARCHAR(30) NOT NULL, email VARCHAR(40) NOT NULL UNIQUE, token VARCHAR(30) UNIQUE, token_time \
            INT(19), PRIMARY KEY (id));'
        }

        connection = self.__connect__()
        with connection.cursor() as cursor:
            cursor.execute('SHOW TABLES')
            db_tables = cursor.fetchone()
            for table in tables:
                if not db_tables:
                    print('\t- Table "' + table + '" not exists! Creating...')
                    cursor.execute(tables[table])
                    continue
                if table not in db_tables:
                    print('\t- Table "' + table + '" not exists! Creating...')
                    cursor.execute(tables[table])
        connection.commit()
        connection.close()
        print('Database checked!\n')

    def __generate_token__(self):
        s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.'
        token = []
        for i in range(0, 30, 1):
            token.append(s[random.randint(0, len(s)-1)])
        return ''.join(token)

    def check_token(self, token):
        if token == 'NULL':
            return 100

        connection = self.__connect__()
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT token_time FROM accounts WHERE token=\'{token}\'')
            t = cursor.fetchone()
            if t:
                if int(time.time()) - int(t) < self.lifetime:
                    connection.close()
                    return 'Valid'
        connection.close()
        return 'Invalid'

    def create_account(self, login, password, email):
        if login == 'NULL' or password == 'NULL' or email == 'NULL':
            return 102
        if len(login) > 20 or len(email) > 40 or len(login) < 4:
            return 201
        if len(password) < 6:
            return 205

        login = login.lower()
        password = hashlib.md5(password.encode(encoding='UTF-8', errors='strict')).hexdigest()
        email = email.lower()

        if not re.match('(^|\s)[-a-z0-9_.]+@([-a-z0-9а-яё]+\.)+[a-zа-яё]{2,6}(\s|$)', email):
            return 203
        if not re.match('^[a-z0-9._-]+$', login):
            return 204

        token = self.__generate_token__()
        token_time = int(time.time())
        id = 0

        connection = self.__connect__()
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM accounts WHERE login=\'{login}\' OR email=\'{email}\'')
            if cursor.fetchall():
                connection.close()
                return 202
            cursor.execute(f'INSERT INTO accounts (login, password, email, token, token_time) VALUES (\'{login}\', \
                \'{password}\', \'{email}\', \'{token}\', {token_time})')
            cursor.execute(f'SELECT id FROM accounts WHERE login=\'{login}\'')
            id = cursor.fetchone()[0]
        connection.commit()
        connection.close()
        return {'id': id, 'token': token, 'token_time': token_time}

    def get_token(self, login, password):
        if login == 'NULL' or password == 'NULL':
            return 102

        password = hashlib.md5(password.encode(encoding='UTF-8', errors='strict')).hexdigest()
        login = login.lower()

        # TODO: add function "check login"
        if not re.match('^[a-z0-9._-]+$', login):
            return 204

        connection = self.__connect__()
        with connection.cursor() as cursor:

            cursor.execute(f'SELECT token,token_time FROM accounts WHERE login=\'{login}\' AND password=\'{password}\'')
            t = cursor.fetchone()

            if not t:
                connection.close()
                return 206

            if time.time() - t['token_time'] < self.lifetime:
                connection.close()
                return {'token': t['token'], 'token_time': t['token_time']}

            token = self.__generate_token__()
            token_time = int(time.time())

            cursor.execute(f'UPDATE accounts SET token = \'{token}\', token_time={token_time} WHERE login=\'{login}\'')
        connection.commit()
        connection.close()
        return {'token': token, 'token_time': token_time}
