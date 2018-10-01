import unittest
import json
import os
from api.app import app
from api.models.db import DB

class APITest(unittest.TestCase):
    def setUp(self):
        self.app=app
        self.dbconnector=DBconfig(host='localhost',user='postgres', dbname='',port=5432,password='sudo')

        print(self.dbconnector.dbname)
        self.dbconnector.drop_all_tables('orders','users','fastfoods')
        self.dbconnector.create_db_tables()
        self.client = self.app.test_client()
        self.user = {
            'username': 'dee',
            'password': 'dee'
        }
     
    def test_create_user(self):
        res=self.client.post('/api/v2/auth/users',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(res.status_code, 200)
        self.assertIn("user created",str(res.data))