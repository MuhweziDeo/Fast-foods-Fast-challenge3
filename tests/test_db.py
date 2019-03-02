import unittest
from api.models.db import DB
from api.models.menu import Menu
from api.models.orders import Orders
from api.models.users import Users


class DBTestCase(unittest.TestCase):
    def setUp(self):
        self.db = DB()
        self.dbusers = Users()
        self.dbmenu = Menu()
        self.dborders = Orders()
        self.db.create_db_tables()

    def test_create_user(self):
        query = self.dbusers.register_user('dee', 'dee')
        self.assertIn('user created', str(query))

    def test_find_user_by_username(self):
        query = self.dbusers.register_user('dee', 'dee')
        self.assertIn('user created', str(query))
        query = self.dbusers.find_by_username('dee')
        self.assertIn('dee', str(query))

    def test_create_meal_option(self):
        query = self.dbmenu.add_meal('pizza', 4000)
        self.assertIn('meal pizza added', str(query))

    def test_get_menu(self):
        query = self.dbmenu.get_menu()
        self.assertIn('Menu', str(query))

    def test_create_order(self):
        query = self.dbusers.register_user('dee', 'dee')
        query = self.dbmenu.add_meal('pizza', 4000)
        query = self.dborders.create_order("location", 4, 1, 'pizza')
        self.assertIn("order placed successfully", str(query))

    def test_get_order_history_for_a_user(self):
        query = self.dbusers.register_user('dee', 'dee')
        query = self.dbmenu.add_meal('pizza', 4000)
        query = self.dborders.create_order("location", 4, 1, 'pizza')
        query = self.dborders.get_order_history_for_a_user(1)
        self.assertIn('orders for user with id 1', str(query))

    def test_get_all_orders(self):
        query = self.dbusers.register_user('dee', 'dee')
        query = self.dbmenu.add_meal('pizza', 4000)
        query = self.dborders.create_order("location", 4, 1, 'pizza')
        query = self.dborders.get_all_orders()
        self.assertIn('All Orders', str(query))

    def test_get_order(self):
        query = self.dbusers.register_user('dee', 'dee')
        query = self.dbmenu.add_meal('pizza', 4000)
        query = self.dborders.create_order("location", 4, 1, 'pizza')
        query = self.dborders.get_order(1)
        self.assertIn('1', str(query))
        self.assertIn('pizza', str(query))

    def test_update_order_status(self):
        query = self.dbusers.register_user('dee', 'dee')
        query = self.dbmenu.add_meal('pizza', 4000)
        query = self.dborders.create_order("location", 4, 1, 'pizza')
        query = self.dborders.update_order_status(1, "Accepted")
        self.assertIn("order status updated", str(query))

    def test_update_meal_option(self):
        query = self.dbmenu.add_meal('pizza', 4000)
        query = self.dbmenu.update_meal(1, 2000, "burger")
        self.assertIn("meal updated", str(query))

    def test_delete_meal_option(self):
        query = self.dbmenu.add_meal('pizza', 4000)
        query = self.dbmenu.delete_meal(1)
        self.assertIn("meal deleted", str(query))

    def tearDown(self):
        print('dropping')
        self.db.drop_all_tables('orders', 'users', 'fastfoods')
