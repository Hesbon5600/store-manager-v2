'''Defining the blueprint and the access routes'''
from flask import Blueprint
from flask_restful import Api
from .views.userviews import UserRegistration, UserLogin
from .views.userviews import Logout, GetUsers, PromoteUser
from .views.saleviews import Sale, SingleSale
from .views.productviews import Product, SingleProduct
v2 = Blueprint('api', __name__, url_prefix='/api/v2')

api = Api(v2)

api.add_resource(UserRegistration, '/auth/signup')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(Logout, '/auth/logout')
api.add_resource(Product, '/products')
api.add_resource(SingleProduct, '/products/<product_id>')
api.add_resource(Sale, '/sales')
api.add_resource(SingleSale, '/sales/<sale_id>')
api.add_resource(PromoteUser, '/users/<user_id>')
api.add_resource(GetUsers, '/users')
