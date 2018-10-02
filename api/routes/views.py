from flask_restplus import Api, Resource, fields
from flask_jwt_extended import jwt_required, JWTManager, create_access_token, get_jwt_identity
from api.app import app
from api.models.db import DB

db = DB(user='postgres', password='sudo',
        dbname=' ', host='localhost')

api = Api(app, prefix='/api/v2', version='2.0', title='Fast-Foods-Api')
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'thisissecretkhahxcahiahiac'

db.create_db_tables()
# db.drop_all_tables('orders','users','fastfoods')

user = api.model('User', {
    'username': fields.String(description="username", required=True, min_length=4),
    'password': fields.String(description="user password", required=True, min_length=4),
    'confirm': fields.String
})

userlogin = api.model('User-login', {
    'username': fields.String(description="username", required=True, min_length=4),
    'password': fields.String(description="user password", required=True, min_length=4)
})


meal = api.model('Meal Option', {
    'meal_name': fields.String(description="meal_name", required=True, min_length=4),
    'price': fields.Integer(description="price", required=True, min_length=4),
})

mealupdate = api.model('Meal Update', {
    'meal_status': fields.String(description="meal_name", required=True, min_length=4),
    'price': fields.Integer(description="price", required=True, min_length=4),
})

order = api.model('Order', {
    'location': fields.String,
    'quantity': fields.Integer,
    'meal': fields.String,
    'user_id': fields.Integer
})

orderstatus = api.model('order-status', {
    "status": fields.String
})


jwt = {'Authorization': {'Authorization Bearer': 'Bearer',
                         'in': 'header',
                         'type': '',
                         'description': 'Bearer <token>'}}


@api.route('/auth/signup')
class Signup(Resource):
    @api.expect(user)
    def post(self):
        data = api.payload
        username = data['username']
        password = data['password']
        confirm_password = data['confirm']
        user = db.find_by_username(username)
        if user is None:
            if confirm_password == password:
                return db.register_user(username, password)
            else:
                return {'message': 'passwords must match '}
        else:
            return {'message': 'username {} already taken'.format(username)}


@api.route('/auth/login')
class Login(Resource):
    @api.expect(userlogin)
    def post(self):
        data = api.payload
        username = data['username']
        attempted_password = data['password']
        user = db.find_by_username(username)
        if user:
            pasword_hash = user[2]
            if db.confirm_password_hash(attempted_password, pasword_hash):
                token = create_access_token(identity=username)
                return {'message': 'You have been Verified',
                        'token': token}
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


@api.route('/meal/<int:meal_id>')
class Meal(Resource):
    @api.expect(mealupdate)
    def put(self, meal_id):
        """update fastfood"""
        meal = db.find_meal_by_id(meal_id)
        if meal:
            data = api.payload
            meal_status = data['meal_status']
            price = data['price']
            return db.update_meal(meal_id, price, meal_status)
        return {'message': 'You are trying to update a meal that doesnt exist',
                "help": 'check and confirm meal with id {} exists'.format(meal_id)}

    def delete(self, meal_id):
        """Delete FastFood"""
        fastfood = db.find_meal_by_id(meal_id)
        if fastfood is None:
            return {'message': 'meal with meal_id "{}" you tried to delete doesnt exit'.format(meal_id)}
        return db.delete_meal(meal_id)


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

    def get(self):
        """Get orders of a specifi user"""
        user_id = 1
        return db.get_order_history_for_a_user(user_id)


@api.route('/orders')
class Orders(Resource):
    def get(self):
        return db.get_all_orders()


@api.route('/orders/<int:orderId>')
class Order(Resource):
    def get(self, orderId):
        return db.get_order(orderId)

    @api.expect(orderstatus)
    def put(self, orderId):
        """ Update order status"""
        order = db.find_order_by_id(orderId)
        if order:
            data = api.payload
            status = data['status']
            return db.update_order_status(orderId, status)
        else:
            return {'message': 'order {} doesnt exist'.format(orderId)}
