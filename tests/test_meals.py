import unittest
import json
from api.app import app
from api.models.db import DB
from api.models.menu import Menu
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
    self.client = self.app.test_client()

    self.admin = {
        'username': 'super',
        'password': 'super'
    }

    self.meal = {
        "meal_name": 'pizza',
        'price': 4000
    }
    self.meal_update = {
        'meal_status': "Accepted",
        "price": 800
    }

  def test_add_meal_option(self):
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
    self.assertIn('meal pizza added', str(res.data))

  def test_get_menu(self):
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

    res = self.client.get('/api/v2/menu')

    self.assertIn("menu", str(res.data))

  def test_update_meal(self):
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
    res = self.client.put('/api/v2/meal/1',
                          data=json.dumps(self.meal_update),
                          content_type="application/json",
                          headers={'Authorization':
                                   'Bearer {}'.format(self.token)}
                          )
    self.assertIn("meal updated", str(res.data))

  def test_update_non_existing_meal(self):
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
    res = self.client.put('/api/v2/meal/111',
                          data=json.dumps(self.meal_update),
                          content_type="application/json",
                          headers={'Authorization':
                                   'Bearer {}'.format(self.token)}
                          )
    self.assertIn(
        "You are trying to update a meal that doesnt exist", str(res.data))

  def test_delete_meal(self):
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
    res = self.client.delete('/api/v2/meal/1',
                             data=json.dumps(self.meal_update),
                             content_type="application/json",
                             headers={'Authorization':
                                      'Bearer {}'.format(self.token)}
                             )

    self.assertIn("meal deleted", str(res.data))

  def tearDown(self):
    print('dropping')
    self.db.drop_all_tables('orders', 'users', 'fastfoods')
