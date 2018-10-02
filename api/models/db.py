import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import os


class DB():
  def __init__(self, host, user, dbname, password):
    if os.getenv('APP_SETTINGS') != "testing":
      dbname = "apimain"
    else:
      dbname = "fastfoods_test"
    try:
      self.connection = psycopg2.connect(
          user='postgres', password='sudo', dbname='', host='localhost')
      self.cur = self.connection.cursor()
      self.connection.autocommit = True
      print('connection succeful {}'.format(dbname))
    except(Exception, psycopg2.DatabaseError) as e:
      print(e)

  def create_db_tables(self):
    queries = (

        """
            CREATE TABLE IF not EXISTS  fastfoods(
              meal_id serial ,
              meal_name varchar(20) not null primary key unique,
              price int not null
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
      return {'message': 'Please choose a another name because username {} already exits'.format(username)}
