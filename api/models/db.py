
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime


class DB():
    def __init__(self):
        '''INIT DB CLASS'''
        try:
            if os.getenv('APP_SETTINGS') == "testing":
                self.connection = psycopg2.connect(
                    'postgresql://postgres:sudo@127.0.0.1:5432/fastfoods_test')
            elif os.getenv('APP_SETTINGS') == "development":
                self.connection = psycopg2.connect(
                    'postgresql://postgres:sudo@127.0.0.1:5432/apimain')
            else:
                self.connection = psycopg2.connect(
                    os.getenv('DATABASE_URL'))

            self.cur = self.connection.cursor()
            self.connection.autocommit = True
        except(Exception, psycopg2.DatabaseError) as e:
            print(e)

    def create_db_tables(self):
        '''CREATE DATABASE TABLES'''
        queries = (

            """
            CREATE TABLE IF not EXISTS  fastfoods(
              meal_id serial ,
              meal_name varchar(20) not null primary key unique,
              price int not null,
              meal_status varchar(30) default 'Available'
            );
            """,
            """
            CREATE TABLE IF not EXISTS  users(
              user_id serial primary key,
              username varchar(25) not null unique,
              password varchar(100) not null,
              admin boolean default false

            );
            """,

            """
            CREATE TABLE IF not EXISTS orders(
              orderid serial primary key,
              user_id int not null,
              meal_name varchar(20) not null,
              location varchar(1000) not null,
              quantity int not null,
              status varchar(20) not null default 'NEW',
              order_date varchar(40) not null,
              FOREIGN KEY (meal_name) REFERENCES fastfoods(meal_name) ON DELETE CASCADE,
              FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE

            );

            """
        )

        for query in queries:
            self.cur.execute(query)
            self.connection.commit()

    def drop_all_tables(self, *tables):
        for table in tables:
            query = 'DROP TABLE IF EXISTS {}'.format(table)
            self.cur.execute(query)
            self.connection.commit()

    def hash_password(self, password):
        '''HASH PASSWORDS'''
        return generate_password_hash(password)

    def confirm_password_hash(self, password, pasword_hash):
        '''CHECK HASHED PASSWORD'''
        return check_password_hash(pasword_hash, password)

    def register_user(self, username, password):
        '''ADD USER '''
        '''by default a normal user has false in admin column'''
        password = self.hash_password(password)
        create_user = "INSERT INTO users(username,password) VALUES ('{}','{}')".format(
            username, password)
        self.cur.execute(create_user)
        return {'message': 'user created'}

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

    def add_meal(self, meal_name, price):
        '''add meal option to menu'''
        query = "INSERT INTO fastfoods(meal_name,price) VALUES('{}',{})".format(
            meal_name, price)
        self.cur.execute(query)
        return {'message': "meal {} added".format(meal_name)}

    def find_meal_by_name(self, meal_name):
        '''find a meal by its name'''
        try:
            query = "SELECT meal_name FROM fastfoods WHERE meal_name='{}'".format(
                meal_name)
            self.cur = self.connection.cursor()
            self.cur.execute(query)
            fastfood = self.cur.fetchone()
            if fastfood:
                meal_name = fastfood[1]
                return meal_name
            else:
                return None
        except(Exception, psycopg2.DatabaseError) as error:
            print(error, 'Failed')
            return {'error': str(error)}

    def get_menu(self):
        '''get meals on menu'''
        query = "SELECT * FROM fastfoods"
        self.cur = self.connection.cursor(cursor_factory=RealDictCursor)
        self.cur.execute(query)
        fastfoods = self.cur.fetchall()
        if fastfoods:
            return {'menu': fastfoods}
        return {'message': 'No Meals available yet on the Menu'}

    '''ORDER OPERATIONS'''

    def create_order(self, location, quantity, user_id, meal):
        '''create an order'''
        try:
            date = str(datetime.utcnow())
            query = "INSERT INTO orders(location,quantity,meal_name,user_id,order_date) VALUES('{}',{},'{}',{},'{}')".format(
                    location, quantity, meal, user_id, date)
            self.cur.execute(query)
            return {'meaasge': 'order placed successfully'}
        except(Exception, psycopg2.DatabaseError) as e:
            '''since meal references meal name in fastfoods
            when a user tries to order a meal not in the table
            it database operation fials because it violates database contraints '''
            return {'message': 'Its Possible meal {} is not on the menu '.format(meal)}

    def get_order_history_for_a_user(self, user_id):
        '''Get order history of a specific user'''
        query = "SELECT orderid,meal_name,quantity,status,order_date FROM orders WHERE user_id='{}'".format(
            user_id)
        self.cur = self.connection.cursor(cursor_factory=RealDictCursor)
        self.cur.execute(query)
        user_orders = self.cur.fetchall()
        if user_orders:
            return {'orders for user with id {}'.format(user_id): user_orders}
        return {'message': 'user with id {} has placed any orders yet'.format(user_id)}

    def get_all_orders(self):
        '''get all orders'''
        query = "SELECT * FROM orders"
        self.cur = self.connection.cursor(cursor_factory=RealDictCursor)
        self.cur.execute(query)
        orders = self.cur.fetchall()
        if orders:
            return {"All Orders": orders}
        return {'message': 'No orders have been placed yet'}

    def get_order(self, orderId):
        '''get order by its ID'''
        query = "SELECT * FROM orders WHERE orderid={}".format(orderId)
        self.cur = self.connection.cursor(cursor_factory=RealDictCursor)
        self.cur.execute(query)
        order = self.cur.fetchone()
        return {'order_details': order}

    def find_order_by_id(self, orderid):
        '''find an order by its ID'''
        query = "SELECT * FROM orders WHERE orderid='{}'".format(orderid)
        self.cur.execute(query)
        order = self.cur.fetchone()
        if order:
            return {'order_details': order}
        return None

    def update_order_status(self, orderId, status):
        '''update the order status of an order'''
        query = "UPDATE orders SET status='{}' WHERE orderid={}".format(
                status, orderId)
        self.cur.execute(query)
        return {'message': 'order status updated'}

    def find_meal_by_id(self, meal_id):
        '''find a meal by its ID'''
        query = "SELECT meal_name FROM fastfoods WHERE meal_id='{}'".format(
                meal_id)
        self.cur = self.connection.cursor()
        self.cur.execute(query)
        fastfood = self.cur.fetchone()
        if fastfood:
            meal_id = fastfood[0]
            return meal_id
        return None

    def update_meal(self, meal_id, price, meal_status):
        '''update meal_status and price of a meal'''
        query = "UPDATE fastfoods SET meal_status='{}',price={} WHERE meal_id={}".format(
                meal_status, price, meal_id)
        self.cur.execute(query)
        return {'message': 'meal updated'}

    def delete_meal(self, meal_id):
        '''delete a meal from the menu by ID'''
        query = 'DELETE From fastfoods WHERE meal_id={}'.format(meal_id)
        self.cur.execute(query)
        return {'message': 'meal deleted'}
