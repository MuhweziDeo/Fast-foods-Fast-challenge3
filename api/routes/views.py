from api.app import app
from flask_restplus import Api, Resource, fields
from api.models.db import DB
db = DB(host="localhost", user="postgres", dbname="", password="sudo")
db.create_db_tables()

api = Api(app, prefix='/api/v2')

user = api.model('User', {
    'username': fields.String(description="meal to be ordered", required=True, min_length=4),
    'password': fields.String(description="meal to be ordered", required=True, min_length=4),
})


@api.route('/auth/signup')
class SignUp(Resource):
    @api.expect(user, code=201)
    def post(self):
        """ Register user"""
        pass
