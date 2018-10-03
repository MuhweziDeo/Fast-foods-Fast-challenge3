import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime


class DB():
    def __init__(self, host, user, dbname, password):
        if os.getenv('APP_SETTINGS') != "testing":
            databasename = "apimain"
        else:
            databasename = "fastfoods_test"
        try:
            self.connection = psycopg2.connect(
                user='postgres', password='sudo', dbname=''.format(databasename), host='localhost')
            self.cur = self.connection.cursor()
            self.connection.autocommit = True
            print('connection succeful {}'.format(databasename))
        except(Exception, psycopg2.DatabaseError) as e:
            print(e)

    def create_db_tables(self):
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
        try:
            for query in queries:
                self.cur.execute(query)
                self.connection.commit()
                print('Tables Created')
        except(Exception, psycopg2.DatabaseError) as error:
            print(error, "Dont Panic But  Table Creation Failed")

    def drop_all_tables(self, *tables):
        try:
            for table in tables:
                query = 'DROP TABLE IF EXISTS {}'.format(table)
                self.cur.execute(query)
                self.connection.commit()
                print(query)
                print("Deleted")
        except(Exception, psycopg2.DatabaseError) as error:
            print(error, 'Failed')

           # users
    def hash_password(self, password):
        return generate_password_hash(password)

    def confirm_password_hash(self, password, pasword_hash):
        return check_password_hash(pasword_hash, password)

    def register_user(self, username, password):
        try:
            password = self.hash_password(password)
            # new_user=User(username,password)
            create_user = "INSERT INTO users(username,password) VALUES ('{}','{}')".format(
                          username, password)
            print(create_user)
            self.cur.execute(create_user)
            # print(new_user)
            return {'message': 'user created'}
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            # return None
            return {'message': 'Unable to create account'}

    def register_admin(self, username, password):
        try:
            password = self.hash_password(password)
            # new_user=User(username,password)
            create_user = "INSERT INTO users(username,password,admin) VALUES ('{}','{}',True)".format(
                          username, password)
            print(create_user)
            self.cur.execute(create_user)
            # print(new_user)
            return {'message': 'admin user created'}
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            # return None
            return {'message': 'Unable to create account'}

    def find_by_username(self, username):
        try:
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
            else:
                return None
        except(Exception, psycopg2.DatabaseError) as e:
            print(e)
            return {'message': 'unable to complete request'}

    def add_meal(self, meal_name, price):
        try:
            query = "INSERT INTO fastfoods(meal_name,price) VALUES('{}',{})".format(
                meal_name, price)
            self.cur.execute(query)
            return {'message': "meal {} added".format(meal_name)}
        except(Exception, psycopg2.DatabaseError) as e:
            print(e)
            return {'error': "Cant Add Meal at the moment"}

    def find_meal_by_name(self, meal_name):
        # find meal by name
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
        # get all meals/menu
        try:
            query = "SELECT * FROM fastfoods"
            self.cur = self.connection.cursor(cursor_factory=RealDictCursor)
            self.cur.execute(query)
            fastfoods = self.cur.fetchall()
            if fastfoods:
                return {'menu': fastfoods}
            else:
                return {'message': 'No Meals available yet on the Menu'}
        except(Exception, psycopg2.DatabaseError) as error:
            print(error, 'Failed')
            return {'error': str(error)}
    # orders

    def create_order(self, location, quantity, user_id, meal):
        # create an order
        try:
            date = str(datetime.utcnow())
            query = "INSERT INTO orders(location,quantity,meal_name,user_id,order_date) VALUES('{}',{},'{}',{},'{}')".format(
                location, quantity, meal, user_id, date)
            self.cur.execute(query)
            return {'meaasge': 'order placed successfully'}
        except(Exception, psycopg2.DatabaseError) as e:
            print(e)
            return {"message": "unable to place order"}

    def get_order_history_for_a_user(self, user_id):
        # get order history of a user
        try:
            query = "SELECT * FROM orders WHERE user_id='{}'".format(user_id)
            self.cur = self.connection.cursor(cursor_factory=RealDictCursor)
            self.cur.execute(query)
            user_orders = self.cur.fetchall()
            if user_orders:
                return {'orders for user with id {}'.format(user_id): user_orders}
            else:
                return {'message': 'user with id {} has placed any orders yet'.format(user_id)}
        except(Exception, psycopg2.DatabaseError) as e:
            print(e)
            return {'message': 'unable to retrive orders'}

    def get_all_orders(self):
        try:
            query = "SELECT * FROM orders"
            self.cur = self.connection.cursor(cursor_factory=RealDictCursor)
            self.cur.execute(query)
            orders = self.cur.fetchall()
            if orders:
                return {"All Orders": orders}
            else:
                return {'message': 'No orders have been placed yet'}
        except(Exception, psycopg2.DatabaseError) as e:
            print(e)
            return {'message': 'unable to retrive orders'}

    def get_order(self, orderId):
        try:
            query = "SELECT * FROM orders WHERE orderid={}".format(orderId)
            self.cur = self.connection.cursor(cursor_factory=RealDictCursor)
            self.cur.execute(query)
            order = self.cur.fetchone()
            # if order:
            return {'order_details': order}
            # else:
            #     return {'message':'order with orderId {} doesnt exist'.format(orderId)}
        except(Exception, psycopg2.DatabaseError) as e:
            print(e)

    def find_order_by_id(self, orderid):
          # find order by id
        try:
            query = "SELECT * FROM orders WHERE orderid='{}'".format(orderid)
            self.cur.execute(query)
            order = self.cur.fetchone()
            if order:
                return {'order_details': order}
            else:
                return None
        except(Exception, psycopg2.DatabaseError) as error:
            print(error, 'Failed')
            return {'error': str(error)}

    def update_order_status(self, orderId, status):
        try:
            query = "UPDATE orders SET status='{}' WHERE orderid={}".format(
                status, orderId)
            self.cur.execute(query)
            print(query)
            return {'message': 'order status updated'}
        except(Exception, psycopg2.DatabaseError) as e:
            print(e)
            return {'message': 'Sorry Unable To Complete Request'}

    def find_meal_by_id(self, meal_id):
        # find meal by id
        try:
            query = "SELECT meal_name FROM fastfoods WHERE meal_id='{}'".format(
                meal_id)
            self.cur = self.connection.cursor()
            self.cur.execute(query)
            fastfood = self.cur.fetchone()
            if fastfood:
                meal_id = fastfood[0]
                return meal_id
            else:
                return None
        except(Exception, psycopg2.DatabaseError) as error:
            print(error, 'Failed')
            return {'error': str(error)}

    def update_meal(self, meal_id, price, meal_status):
        # update meal
        try:
            query = "UPDATE fastfoods SET meal_status='{}',price={} WHERE meal_id={}".format(
                meal_status, price, meal_id)
            self.cur.execute(query)
            print(query)
            return {'message': 'meal updated'}
        except(Exception, psycopg2.DatabaseError) as e:
            print(e)
            return {'Message': 'Unable to complete Request'}

    def delete_meal(self, meal_id):
        # delete fastfood
        try:
            query = 'DELETE From fastfoods WHERE meal_id={}'.format(meal_id)
            self.cur.execute(query)
            return {'message': 'meal deleted'}
        except(Exception, psycopg2.DatabaseError) as e:
            print(e)
            return {'message': "Something Went Wrong Unable to Complete request"}
