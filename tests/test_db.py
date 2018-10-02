import unittest
from api.models.db import DB


class DBTestCase(unittest.TestCase):
    def setUp(self):
        self.db = DB(host='localhost', user='postgres',
                     dbname='', password='sudo')
        self.db.drop_all_tables('orders', 'users', 'fastfoods')
        self.db.create_db_tables()

    def test_create_user(self):
        query = self.db.register_user('dee', 'dee')
        self.assertIn('user created', str(query))