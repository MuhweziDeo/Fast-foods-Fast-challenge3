from api.models.db import DB
import psycopg2
from psycopg2.extras import RealDictCursor


class Menu(DB):
    def __init__(self):
        DB.__init__(self)

    def add_meal(self, meal_name, price):
        '''add meal option to menu'''
        query = "INSERT INTO fastfoods(meal_name,price) VALUES('{}',{})".format(
            meal_name, price)
        self.cur.execute(query)
        return {'message': "meal {} added".format(meal_name)}

    def find_meal_by_name(self, meal_name):
        '''find a meal by its name'''
        query = "SELECT meal_name FROM fastfoods WHERE meal_name='{}'".format(
                meal_name)
        self.cur = self.connection.cursor()
        self.cur.execute(query)
        fastfood = self.cur.fetchone()
        if fastfood:
            meal_name = fastfood[1]
            return meal_name
        return None

    def get_menu(self):
        '''get meals on menu'''
        query = "SELECT * FROM fastfoods"
        self.real_dic_cursor(query)
        fastfoods = self.cur.fetchall()
        if fastfoods:
            return {'menu': fastfoods}
        return {'message': 'No Meals available yet on the Menu'}

    def find_meal_by_id(self, meal_id):
        '''find a meal by its ID'''
        query1 = "SELECT meal_name FROM fastfoods WHERE meal_id='{}'".format(
            meal_id)
        self.cur = self.connection.cursor()
        self.cur.execute(query1)
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
