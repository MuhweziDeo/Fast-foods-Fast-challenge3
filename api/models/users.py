from api.models.db import DB
from werkzeug.security import generate_password_hash, check_password_hash


class Users(DB):
    def __init__(self):
        DB.__init__(self)

    def register_user(self, username, password):
        '''ADD USER '''
        '''by default a normal user has false in admin column'''
        password = self.hash_password(password)
        create_user = "INSERT INTO users(username,password) VALUES ('{}','{}')".format(
            username, password)
        self.cur.execute(create_user)
        return {'message': 'user created'}

    def hash_password(self, password):
        '''HASH PASSWORDS'''
        return generate_password_hash(password)

    def confirm_password_hash(self, password, pasword_hash):
        '''CHECK HASHED PASSWORD'''
        return check_password_hash(pasword_hash, password)

    def register_admin(self, username, password):
        '''ADD ADMIN USER'''
        password = self.hash_password(password)
        create_user = "INSERT INTO users(username,password,admin) VALUES ('{}','{}',True)".format(
            username, password)
        self.cur.execute(create_user)
        return {'message': 'admin user created'}

    def find_by_username(self, username):
        '''find user by thier username'''
        query = "SELECT * from users where username='{}'".format(username)
        self.cur = self.connection.cursor()
        self.cur.execute(query)
        user = self.cur.fetchone()
        if user:
            user_id = user[0]
            username = user[1]
            password = user[2]
            admin = user[3]
            return user_id, username, password, admin
        return None
