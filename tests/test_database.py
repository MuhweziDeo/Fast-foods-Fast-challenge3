import unittest
from api.models.db import DB


class DBTestCase(unittest.TestCase):
    def setUp(self):
        self.db = DB(
            host='localhost', user='postgres', dbname='', port=5432, password='Adeo256.')
        self.dbconnector.drop_all_tables('orders', 'users', 'fastfoods')
        self.dbconnector.create_db_tables()

    def test_create_user(self):
        query = self.dbconnector.register_user('dee', 'dee')
        self.assertIn('user created', str(query))

    def tearDown(self):
        self.dbconnector.drop_all_tables('orders', 'fastfoods', 'users',)
        print('deleted')
