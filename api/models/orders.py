from api.models.db import DB
import psycopg2
from datetime import datetime
from psycopg2.extras import RealDictCursor


class Orders(DB):
    def __init__(self):
        DB.__init__(self)

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
        # self.cur = self.connection.cursor(cursor_factory=RealDictCursor)
        # self.cur.execute(query)
        self.real_dic_cursor(query)
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
