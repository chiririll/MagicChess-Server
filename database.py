import pymysql


class Database:

    def __init__(self, ip, user, passw, db):
        #self.connection = pymysql.connect(ip, user, passw, db)
        pass

    #def check(self):
    #    with self.connection:
    #        cursor = self.connection.cursor()

    def check_token(self, token):
        if token == 'ACCBDA':
            return True
        return False
