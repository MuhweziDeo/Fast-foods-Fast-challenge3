import unittest
import json
from api.app import app
from api.models.db import DB
from datetime import datetime


class DatabaseTest(unittest.TestCase):

  def setUp(self):
    self.app = app
    self.db = DB()
    self.db.create_db_tables()
    self.client = self.app.test_client()
    self.user = {
        'username': 'dee',
        'password': 'dee',
        'confirm': 'dee'
    }
    self.admin_reg = {
        'username': 'admin',
        'password': 'admin',
        'confirm': 'admin'
    }
    self.admin = {
        'username': 'admin',
        'password': 'admin'
    }
    self.invalid_confirm_password = {
        'username': 'dee',
        'password': 'dee',
        'confirm': 'deeooo'
    }
    self.invalid_username = {
        'username': 'deodee',
        'password': 'dee',
        'confirm': 'dee'
    }
    self.invalid_password = {
        'username': 'dee',
        'password': 'deodee'
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
        "location": "kla",
        "quantity": 4,
        "meal": "pizza"
    }
    self.order_status = {
        "status": "Accepted"
    }

  def test_create_order(self):
    res = self.client.post('/api/v2/auth/admin',
                           data=json.dumps(self.admin_reg),
                           content_type='application/json'
                           )
    res_login = self.client.post('/api/v2/auth/login',
                                 data=json.dumps(self.admin),
                                 content_type='application/json')
    login_data = res_login.json
    self.token = login_data['token']

    res = self.client.post('/api/v2/menu',
                           data=json.dumps(self.meal),
                           content_type="application/json",
                           headers={'Authorization':
                                    'Bearer {}'.format(self.token)})

    res = self.client.post('/api/v2/auth/signup',
                           data=json.dumps(self.user),
                           content_type='application/json'
                           )
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
    self.assertIn("order placed successfully", str(res.data))

  def test_get_orders_for_a_user(self):
    res = self.client.post('/api/v2/auth/admin',
                           data=json.dumps(self.admin_reg),
                           content_type='application/json'
                           )
    res_login = self.client.post('/api/v2/auth/login',
                                 data=json.dumps(self.admin),
                                 content_type='application/json')
    login_data = res_login.json
    self.token = login_data['token']

    res = self.client.post('/api/v2/menu',
                           data=json.dumps(self.meal),
                           content_type="application/json",
                           headers={'Authorization':
                                    'Bearer {}'.format(self.token)})

    res = self.client.post('/api/v2/auth/signup',
                           data=json.dumps(self.user),
                           content_type='application/json'
                           )
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
    res = self.client.get('/api/v2/users/orders',
                          headers={'Authorization':
                                   'Bearer {}'.format(self.token)}
                          )
    self.assertIn('orders for user with id 2', str(res.data))

  def test_get_all_orders(self):
    res = self.client.post('/api/v2/auth/admin',
                           data=json.dumps(self.admin_reg),
                           content_type='application/json'
                           )
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

    res = self.client.post('/api/v2/auth/signup',
                           data=json.dumps(self.user),
                           content_type='application/json'
                           )
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

    res = self.client.get('/api/v2/orders',
                          headers={'Authorization':
                                   'Bearer {}'.format(self.token_admin)})

    self.assertIn("All Orders", str(res.data))

  def test_get_order(self):
    res = self.client.post('/api/v2/auth/admin',
                           data=json.dumps(self.admin_reg),
                           content_type='application/json'
                           )
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

    res = self.client.post('/api/v2/auth/signup',
                           data=json.dumps(self.user),
                           content_type='application/json'
                           )
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
    res = self.client.post('/api/v2/auth/admin',
                           data=json.dumps(self.admin_reg),
                           content_type='application/json'
                           )
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
    res = self.client.post('/api/v2/auth/signup',
                           data=json.dumps(self.user),
                           content_type='application/json'
                           )
    res = self.client.post('/api/v2/menu',
                           data=json.dumps(self.meal),
                           content_type="application/json"
                           )
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
