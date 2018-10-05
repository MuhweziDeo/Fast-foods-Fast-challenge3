from flask_restplus import Resource, fields
from api.routes.views import api, jwt, admin_required
from api.models.users import Users
dbusers = Users()


def register_super_admin(username, password):
    if dbusers.find_by_username(username) == None:
        dbusers.register_admin(username, password)
    return 'super'


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


@api.route('/auth/admin')
class AdminRegistration(Resource):
    @admin_required
    @api.expect(user, validate=True)
    def post(self):
        data = api.payload
        username = data['username']
        password = data['password']
        confirm_password = data['confirm']
        user = dbusers.find_by_username(username)
        if user is None:
            if confirm_password == password:
                return dbusers.register_admin(username, password), 201
            return {'message': 'passwords must match '}
        return {'message': 'username {} already taken'.format(username)}


@api.route('/auth/signup')
class Signup(Resource):
    @api.expect(user, validate=True)
    def post(self):
        data = api.payload
        username = data['username']
        password = data['password']
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
        username = data['username']
        attempted_password = data['password']
        user = dbusers.find_by_username(username)
        if user:
            pasword_hash = user[2]
            if dbusers.confirm_password_hash(attempted_password, pasword_hash):
                token = create_access_token(identity=username)
                return {'message': 'You have been Verified',
                        'token': token}, 201
            return {'message': 'password verification failed'}, 400
        return {'message': 'username {} deosnt exist'.format(username)}, 404
