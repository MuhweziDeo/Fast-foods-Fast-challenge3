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

    def test_create_user(self):
        res = self.client.post('/auth/users',
                               data=json.dumps(self.user),
                               content_type='application/json'
                               )
        self.assertEqual(res.status_code, 200)
        self.assertIn("user created", str(res.data))