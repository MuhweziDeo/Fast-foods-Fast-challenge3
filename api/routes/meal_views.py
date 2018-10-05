from flask_restplus import Resource, fields
from api.routes.views import api, jwt
from api.models.menu import Menu
dbmenu = Menu()

meal = api.model('Meal Option', {
    'meal_name': fields.String(description="meal_name", required=True, min_length=4),
    'price': fields.Integer(description="price", required=True, min_length=4),
})

mealupdate = api.model('Meal Update', {
    'meal_status': fields.String(description="meal_name", required=True, min_length=4),
    'price': fields.Integer(description="price", required=True, min_length=4),
})


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
            meal_status = data['meal_status']
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


@api.route('/menu')
class Menu(Resource):
    @admin_required
    @api.doc(params=jwt)
    @api.expect(meal, validate=True)
    def post(self):
        data = api.payload
        meal_name = data['meal_name']
        price = data['price']
        meal = dbmenu.find_meal_by_name(meal_name)
        if meal:
            return {'message': 'meal with name {} already exists'.format(meal_name)}, 404
        return dbmenu.add_meal(meal_name, price)

    def get(self):
        return dbmenu.get_menu()
