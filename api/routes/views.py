from flask_restplus import Api, Resource, fields
from api.app import app
from api.models.db import DB

db = DB(user='postgres', password='sudo',
        dbname=' ', host='localhost')

api = Api(app, version='2.0', title='Fast-Foods-Api')


db.create_db_tables()
# db.drop_all_tables('orders','users','fastfoods')

user = api.model('User', {
    'username': fields.String(description="username", required=True, min_length=4),
    'password': fields.String(description="user password", required=True, min_length=4),
})


@api.route('/auth/users')
class Signup(Resource):
    @api.expect(user)
    def post(self):
        data = api.payload
        username = data['username']
        password = data['password']
        return db.register_user(username, password)
