
import psycopg2
from psycopg2.extras import RealDictCursor

import os
from datetime import datetime


class DB():
  def __init__(self):
    """INIT DB CLASS"""
    try:
      if os.getenv('APP_SETTINGS') == "testing":
        self.connection = psycopg2.connect(
            'postgresql://postgres:sudo@127.0.0.1:5432/fastfoods_test')
      elif os.getenv('APP_SETTINGS') == "development":
        self.connection = psycopg2.connect(
            'postgresql://postgres:@127.0.0.1:5432/flasky')
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

  def real_dic_cursor(self, query):
    self.cur = self.connection.cursor(cursor_factory=RealDictCursor)
    self.cur.execute(query)
