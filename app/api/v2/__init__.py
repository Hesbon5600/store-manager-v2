from flask import Blueprint
from flask_restful import Api
from .views import Sale, UserRegistration, UserLogin, Product, SingleProduct, SingleSale
v2 = Blueprint('api', __name__, url_prefix='/api/v2')

api = Api(v2)

api.add_resource(UserRegistration, '/auth/signup')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(Product, '/products')
api.add_resource(SingleProduct, '/products/<productID>')
api.add_resource(Sale, '/sales')
api.add_resource(SingleSale, '/sales/<saleID>')
