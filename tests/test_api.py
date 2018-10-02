import unittest
import json
from api.app import app
from api.models.db import DB


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.db = DB(host='localhost', user='postgres',
                     dbname='', password='sudo')
        self.db.drop_all_tables('orders', 'users', 'fastfoods')
        self.db.create_db_tables()
        self.client = self.app.test_client()
        self.user = {
            'username': 'dee',
            'password': 'dee'
        }
        self.invalid_username = {
            'username': 'deodee',
            'password': 'dee'
        }

    def test_create_user(self):
        res = self.client.post('/api/v2/auth/signup',
                               data=json.dumps(self.user),
                               content_type='application/json'
                               )
        self.assertEqual(res.status_code, 200)
        self.assertIn("user created", str(res.data))

    def test_user_login(self):
        res = self.client.post('/api/v2/auth/signup',
                               data=json.dumps(self.user),
                               content_type='application/json'
                               )
        self.assertIn("user created", str(res.data))
        res_login = self.client.post('/api/v2/auth/login',
                                     data=json.dumps(self.user),
                                     content_type='application/json')
        self.assertIn('You have been Verified', str(res_login.data))

    def test_invalid_username_login(self):
        res = self.client.post('/api/v2/auth/signup',
                               data=json.dumps(self.user),
                               content_type='application/json'
                               )
        self.assertIn("user created", str(res.data))
        res_login = self.client.post('/api/v2/auth/login',
                                     data=json.dumps(self.invalid_username),
                                     content_type='application/json')
        self.assertIn('username deodee deosnt exist', str(res_login.data))
