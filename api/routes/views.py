from flask_restplus import Api, Resource, fields
from api.app import app
from api.models.db import DB

db = DB(user='postgres', password='sudo',
        dbname=' ', host='localhost')

api = Api(app, prefix='/api/v2', version='2.0', title='Fast-Foods-Api')


db.create_db_tables()
# db.drop_all_tables('orders','users','fastfoods')

user = api.model('User', {
    'username': fields.String(description="username", required=True, min_length=4),
    'password': fields.String(description="user password", required=True, min_length=4),
})

meal = api.model('Meal Option', {
    'meal_name': fields.String(description="meal_name", required=True, min_length=4),
    'price': fields.Integer(description="price", required=True, min_length=4),
})

order = api.model('Order', {
    'location': fields.String,
    'quantity': fields.Integer,
    'meal': fields.String,
    'user_id': fields.Integer
})


@api.route('/auth/signup')
class Signup(Resource):
    @api.expect(user)
    def post(self):
        data = api.payload
        username = data['username']
        password = data['password']
        user = db.find_by_username(username)
        if user is None:
            return db.register_user(username, password)
        else:
            return {'message': 'username {} already taken'.format(username)}


@api.route('/auth/login')
class Login(Resource):
    @api.expect(user)
    def post(self):
        data = api.payload
        username = data['username']
        attempted_password = data['password']
        user = db.find_by_username(username)
        if user:
            pasword_hash = user[2]
            if db.confirm_password_hash(attempted_password, pasword_hash):
                return {'message': 'You have been Verified'}
            else:
                return {'message': 'password verification failed'}
        else:
            return {'message': 'username {} deosnt exist'.format(username)}


@api.route('/menu')
class Menu(Resource):
    @api.expect(meal)
    def post(self):
        data = api.payload
        meal_name = data['meal_name']
        price = data['price']
        meal = db.find_meal_by_name(meal_name)
        if meal:
            return {'message': 'meal with name {} already exists'.format(meal_name)}
        return db.add_meal(meal_name, price)

    def get(self):
        return db.get_menu()


@api.route('/users/orders')
class UserOrders(Resource):
    @api.expect(order)
    def post(self):
        """ Post An Order"""
        data = api.payload
        meal = data['meal']
        location = data['location']
        quantity = data['quantity']
        user_id = data['user_id']
        return db.create_order(location, quantity, user_id, meal)
# orders


@api.route('/users/orders')
class UserOrders(Resource):
    def get(self):
        """Get orders of a specifi user"""
        user_id = 1
        return db.get_order_history_for_a_user(user_id)
