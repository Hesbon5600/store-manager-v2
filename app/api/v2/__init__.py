from flask import Blueprint
from flask_restful import Api
from .views import UserRegistration
v2 = Blueprint('api2', __name__, url_prefix='/api/v2')

api = Api(v2)

api.add_resource(UserRegistration, '/auth/signup')