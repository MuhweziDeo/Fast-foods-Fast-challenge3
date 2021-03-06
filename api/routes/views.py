from flask import jsonify
from flask_restplus import Api, Resource, fields
from flask_jwt_extended import jwt_required, JWTManager, create_access_token, get_jwt_identity, verify_jwt_in_request
from api.app import app
from api.models.db import DB
from api.models.users import Users
from api.models.menu import Menu
from api.models.orders import Orders
from functools import wraps
import os
db = DB()
dbusers = Users()
dbmenu = Menu()
dborder = Orders()

api = Api(app, prefix='/api/v2', version='2.0', title='Fast-Foods-Api')
jwt = JWTManager(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db.create_db_tables()


def register_super_admin(username, password):
    if dbusers.find_by_username(username) == None:
        dbusers.register_admin(username, password)
    return False


register_super_admin('super', 'super')

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
    'location': fields.String(description="location", required=True, min_length=4),
    'quantity': fields.Integer(description="quantity", required=True, min_length=4),
    'meal': fields.String(description="meal_name", required=True, min_length=4)
})

orderstatus = api.model('order-status', {
    "status": fields.String(description="status", required=True, min_length=4)
})


jwt = {'Authorization': {'Authorization Bearer': 'Bearer',
                         'in': 'header',
                         'type': '',
                         'description': 'Bearer <token>'}}


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        user = dbusers.find_by_username(current_user)
        admin = user[3]
        if admin != True:
            return {'message': 'You cant preform this action because you are unauthorised'}, 401

        return f(*args, **kwargs)

    return wrapper


@api.route('/auth/admin')
class AdminRegistration(Resource):
    @admin_required
    @api.expect(user, validate=True)
    def post(self):
        data = api.payload
        username = data['username'].strip()
        password = data['password'].strip()
        confirm_password = data['confirm']
        user = dbusers.find_by_username(username)
        if user is None:
            if confirm_password == password:
                return dbusers.register_admin(username, password), 201
            return {'message': 'passwords must match '}
        return {'message': 'username {} already taken'.format(username)}


@api.route('/auth/signup')
class Signup(Resource):
    @api.expect(user)
    def post(self):
        data = api.payload
        username = data['username'].strip()
        password = data['password'].strip()
        confirm_password = data['confirm']
        user = dbusers.find_by_username(username)
        if user is None:
            if confirm_password == password:
                return dbusers.register_user(username, password)
            return {'message': 'passwords must match '}
        return {'message': 'username {} already taken'.format(username)}


@api.route('/auth/login')
class Login(Resource):
    @api.expect(userlogin)
    def post(self):
        data = api.payload
        username = data['username'].strip()
        attempted_password = data['password'].strip()
        user = dbusers.find_by_username(username)
        if user:
            pasword_hash = user[2]
            if dbusers.confirm_password_hash(attempted_password, pasword_hash):
                token = create_access_token(identity=username)
                return {'message': 'You have been Verified',
                        'token': token,'username':username}, 201
            return {'message': 'password verification failed'}, 400
        return {'message': 'username {} deosnt exist'.format(username)}, 404


@api.route('/menu')
class Menu(Resource):
    @admin_required
    @api.doc(params=jwt)
    @api.expect(meal, validate=True)
    def post(self):
        data = api.payload
        meal_name = data['meal_name'].strip()
        price = data['price']
        meal = dbmenu.find_meal_by_name(meal_name)
        if meal:
            return {'message': 'meal with name {} already exists'.format(meal_name)}, 404
        return dbmenu.add_meal(meal_name, price)

    def get(self):
        return dbmenu.get_menu()


@api.route('/meal/<int:meal_id>')
class Meal(Resource):
    @admin_required
    @api.doc(params=jwt)
    @api.expect(mealupdate, validate=True)
    def put(self, meal_id):
        """update fastfood"""
        meal = dbmenu.find_meal_by_id(meal_id)
        if meal:
            data = api.payload
            meal_status = data['meal_status'].strip()
            price = data['price']
            return dbmenu.update_meal(meal_id, price, meal_status)
        return {'message': 'You are trying to update a meal that doesnt exist',
                "help": 'check and confirm meal with id {} exists'.format(meal_id)}, 404

    @admin_required
    @api.doc(params=jwt)
    def delete(self, meal_id):
        """Delete FastFood"""
        fastfood = dbmenu.find_meal_by_id(meal_id)
        if fastfood is None:
            return {'message': 'meal with meal_id "{}" you tried to delete doesnt exit'.format(meal_id)}, 404
        return dbmenu.delete_meal(meal_id)


@api.route('/users/orders')
class UserOrders(Resource):
    @jwt_required
    @api.doc(params=jwt)
    @api.expect(order, validate=True)
    def post(self):
        """ Post An Order"""
        data = api.payload
        meal = data['meal'].strip()
        location = data['location'].strip()
        quantity = data['quantity']
        current_user = get_jwt_identity()
        user = dbusers.find_by_username(current_user)
        user_id = user[0]
        return dborder.create_order(location, quantity, user_id, meal), 201

    @jwt_required
    @api.doc(params=jwt)
    def get(self):
        """Get orders of a specific user"""
        current_user = get_jwt_identity()
        user = dbusers.find_by_username(current_user)
        user_id = user[0]
        return dborder.get_order_history_for_a_user(user_id), 200


@api.route('/orders')
class Orders(Resource):
    @admin_required
    @api.doc(params=jwt)
    def get(self):
        '''Get All Orders'''
        return dborder.get_all_orders(), 200


@api.route('/orders/<int:orderId>')
class Order(Resource):
    @admin_required
    @api.doc(params=jwt)
    def get(self, orderId):
        '''Get one order'''
        order = dborder.find_order_by_id(orderId)
        if order:
            return dborder.get_order(orderId), 200
        return {'message': 'order with Id {} doesnt exist'.format(orderId)}, 404

    @api.expect(orderstatus, validate=True)
    @jwt_required
    @api.doc(params=jwt)
    def put(self, orderId):
        """ Update order status"""
        order = dborder.find_order_by_id(orderId)
        if order:
            data = api.payload
            status = data['status'].strip()
            return dborder.update_order_status(orderId, status), 201
        return {'message': 'order {} doesnt exist'.format(orderId)}


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message': "Hey The URL you Tried to Acess Doesnt Exist on the server"}), 404


@api.errorhandler
def error_handler(error):
    return {'message': str(error)}, getattr(error, 'code', 500)
