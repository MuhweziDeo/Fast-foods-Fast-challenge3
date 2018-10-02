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

    def test_find_user_by_username(self):
        query = self.db.register_user('dee', 'dee')
        self.assertIn('user created', str(query))
        query = self.db.find_by_username('dee')
        self.assertIn('dee', str(query))

    def test_create_meal_option(self):
        query = self.db.add_meal('pizza', 4000)
        self.assertIn('meal pizza added', str(query))

    def test_get_menu(self):
        query = self.db.get_menu()
        self.assertIn('Menu', str(query))

    def test_create_order(self):
        query = self.db.register_user('dee', 'dee')
        query = self.db.add_meal('pizza', 4000)
        query = self.db.create_order("location", 4, "pizza", 1)
        self.assertIn("order placed successfully", str(query))
