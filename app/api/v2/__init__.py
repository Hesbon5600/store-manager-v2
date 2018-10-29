from flask import Blueprint
from flask_restful import Api
from .views import UserRegistration, UserLogin, Product
v2 = Blueprint('api', __name__, url_prefix='/api/v2')

api = Api(v2)

api.add_resource(UserRegistration, '/auth/signup')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(Product, '/products')
