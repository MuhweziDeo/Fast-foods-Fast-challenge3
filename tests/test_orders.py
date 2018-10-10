import unittest
import json
from api.app import app
from api.models.db import DB
from api.models.menu import Menu
from api.models.orders import Orders
from api.models.users import Users
from datetime import datetime


class DatabaseTest(unittest.TestCase):
  def setUp(self):
    self.app = app
    self.db = DB()
    self.db.create_db_tables()
    self.dbmenu = Menu()
    self.dbuser = Users()
    self.dbuser.register_admin('super', 'super')
    self.dbuser.register_user('deee', 'deee')
    self.dbmenu.add_meal('pizza', 4000)
    self.client = self.app.test_client()

    self.admin = {
        'username': 'super',
        'password': 'super'
    }
    self.user = {
        'username': 'deee',
        'password': 'deee'
    }

    self.meal = {
        "meal_name": 'pizza',
        'price': 4000
    }
    self.meal_update = {
        'meal_status': "Accepted",
        "price": 800
    }
    self.order = {
        "location": "bunga",
        "quantity": 4,
        "meal": "pizza"
    }
    self.order_status = {
        "status": "Accepted"
    }

  def test_create_order(self):
    '''login  user'''
    res_login = self.client.post('/api/v2/auth/login',
                                 data=json.dumps(self.user),
                                 content_type='application/json')
    login_data = res_login.json
    '''get authentication token'''
    self.token = login_data['token']
    '''create order'''
    res = self.client.post('/api/v2/users/orders',
                           data=json.dumps(self.order),
                           content_type="application/json",
                           headers={'Authorization':
                                    'Bearer {}'.format(self.token)}
                           )
    self.assertIn("order placed successfully", str(res.data))

  def test_get_orders_for_a_user(self):
    '''login admin user'''
    res_login = self.client.post('/api/v2/auth/login',
                                 data=json.dumps(self.admin),
                                 content_type='application/json')
    login_data = res_login.json
    self.token = login_data['token']
    '''add meal using admin token'''
    res = self.client.post('/api/v2/menu',
                           data=json.dumps(self.meal),
                           content_type="application/json",
                           headers={'Authorization':
                                    'Bearer {}'.format(self.token)})
    '''login user'''
    res_login = self.client.post('/api/v2/auth/login',
                                 data=json.dumps(self.user),
                                 content_type='application/json')
    login_data = res_login.json
    '''get user token'''
    self.token = login_data['token']
    '''create order using admin token'''
    res = self.client.post('/api/v2/users/orders',
                           data=json.dumps(self.order),
                           content_type="application/json",
                           headers={'Authorization':
                                    'Bearer {}'.format(self.token)}
                           )
    '''get orders of user with Id 2'''
    res = self.client.get('/api/v2/users/orders',
                          headers={'Authorization':
                                   'Bearer {}'.format(self.token)}
                          )
    self.assertIn('orders for user with id 2', str(res.data))

  def test_get_all_orders(self):
    '''login admin user'''
    res_login = self.client.post('/api/v2/auth/login',
                                 data=json.dumps(self.admin),
                                 content_type='application/json')
    login_data = res_login.json
    '''get admin token'''
    self.token_admin = login_data['token']
    '''create meal using admin token'''
    res = self.client.post('/api/v2/menu',
                           data=json.dumps(self.meal),
                           content_type="application/json",
                           headers={'Authorization':
                                    'Bearer {}'.format(self.token_admin)})
    '''login normal user to post order'''
    res_login = self.client.post('/api/v2/auth/login',
                                 data=json.dumps(self.user),
                                 content_type='application/json')
    login_data = res_login.json
    self.token = login_data['token']
    '''create order using user token'''
    res = self.client.post('/api/v2/users/orders',
                           data=json.dumps(self.order),
                           content_type="application/json",
                           headers={'Authorization':
                                    'Bearer {}'.format(self.token)}
                           )
    '''get all orders using admin token'''
    res = self.client.get('/api/v2/orders',
                          headers={'Authorization':
                                   'Bearer {}'.format(self.token_admin)})

    self.assertIn("All_Orders", str(res.data))

  def test_get_order(self):
    res_login = self.client.post('/api/v2/auth/login',
                                 data=json.dumps(self.admin),
                                 content_type='application/json')
    login_data = res_login.json
    self.token_admin = login_data['token']

    res = self.client.post('/api/v2/menu',
                           data=json.dumps(self.meal),
                           content_type="application/json",
                           headers={'Authorization':
                                    'Bearer {}'.format(self.token_admin)})
    res_login = self.client.post('/api/v2/auth/login',
                                 data=json.dumps(self.user),
                                 content_type='application/json')
    login_data = res_login.json
    self.token = login_data['token']

    res = self.client.post('/api/v2/users/orders',
                           data=json.dumps(self.order),
                           content_type="application/json",
                           headers={'Authorization':
                                    'Bearer {}'.format(self.token)}
                           )
    res_order = self.client.get('/api/v2/orders/1', headers={'Authorization':
                                                             'Bearer {}'.format(self.token_admin)})

    self.assertIn("pizza", str(res_order.data))

  def test_update_order_status(self):

    res_login = self.client.post('/api/v2/auth/login',
                                 data=json.dumps(self.admin),
                                 content_type='application/json')
    login_data = res_login.json
    self.token_admin = login_data['token']

    res = self.client.post('/api/v2/menu',
                           data=json.dumps(self.meal),
                           content_type="application/json",
                           headers={'Authorization':
                                    'Bearer {}'.format(self.token_admin)})

    res_login = self.client.post('/api/v2/auth/login',
                                 data=json.dumps(self.user),
                                 content_type='application/json')
    login_data = res_login.json
    self.token = login_data['token']

    res = self.client.post('/api/v2/users/orders',
                           data=json.dumps(self.order),
                           content_type="application/json",
                           headers={'Authorization':
                                    'Bearer {}'.format(self.token)}
                           )

    res_order = self.client.put('/api/v2/orders/1',
                                data=json.dumps(self.order_status),
                                content_type="application/json",
                                headers={'Authorization':
                                         'Bearer {}'.format(self.token_admin)}
                                )
    self.assertIn("order status updated", str(res_order.data))

  def tearDown(self):
    print('dropping')
    self.db.drop_all_tables('orders', 'users', 'fastfoods')
