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
