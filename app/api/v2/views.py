from functools import wraps
from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api
from instance.config import app_config
import jwt
from .models import *
from .utils import *
from werkzeug.security import check_password_hash
import datetime


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_obj = User()
        users = user_obj.get_all_users()
        token = None
        current_user = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({
                'Message': 'Token is missing, You must login first'
            }), 401)
        try:
            data = jwt.decode(
                token, app_config['development'].SECRET_KEY, algorithms=['HS256'])

            for user in users:
                if user['username'] == data['username']:
                    current_user = user
        except Exception as e:
            print(e)
            return make_response(jsonify({'Message': 'Token is invalid'}),
                                 403)
        return f(current_user, *args, **kwargs)
    return decorated


class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({
                'Status': 'Failed',
                'Message': "No signup data provided"
            }), 400)

        validate = ValidateUser(data)
        validate.validate_user_details()
        user = User(data)
        user.save_user()
        return make_response(jsonify({
            'Status': 'Ok',
            'Message': "User '" + data['username'] +
            "' successfully registered as '" + data['role'],
        }), 201)


class UserLogin(Resource):
    def post(self):
        self.user_obj = User.get_all_users(self)
        data = request.get_json()
        username = data['username']
        password = data['password']

        if not data or not username or not password:
            return make_response(jsonify({
                                         'Status': 'Failed',
                                         'Message': "Login required"
                                         }), 400)

        for user in self.user_obj:
            if user['username'] == username and check_password_hash(user["password"],
                                                                    password):
                token = jwt.encode({'username': user['username'],
                                    'exp': datetime.datetime.utcnow() +
                                    datetime.timedelta(minutes=3000)},
                                   app_config['development'].SECRET_KEY, algorithm='HS256')
                return make_response(jsonify({
                                             'token': token.decode('UTF-8')
                                             }), 200)

        return make_response(jsonify({
            'Status': 'Failed',
            'Message': "No such user found. Check your login credentials"
        }), 404)


class Product(Resource):
    # Get all products
    @token_required
    def get(current_user, self):
        self.prod_obj = PostProduct.get_all_products(self)

        if current_user:
            if len(self.prod_obj) < 1:
                response = make_response(jsonify({
                    'Status': 'Failed',
                    'Message': "No avilable products"
                }), 404)
            else:
                response = make_response(jsonify({
                    'Status': 'Ok',
                    'Message': "Success",
                    'My products': self.prod_obj
                }), 200)
        else:
            response = make_response(jsonify({
                'Status': 'Failed',
                'Message': "You must first login"
            }), 401)
        return response

    @token_required
    def post(current_user, self):
        data = request.get_json()
        if not data or "title" not in data or 'category' not in data or 'description' not in data or 'price' not in data or 'lower_inventory' not in data or 'quantity' not in data:
            return make_response(jsonify({
                'Status': 'Failed',
                'Message': "Chech your input"
            }), 401)
        if current_user and current_user['role'] != "admin":
            return make_response(jsonify({
                'Status': 'Failed',
                'Message': "You must be an admin"
            }), 401)
        if current_user and current_user['role'] == "admin":
            valid_product = ValidateProduct(data)
            valid_product.validate_duplicates()
            valid_product.validate_product_details()
            product = PostProduct()
            product.save_product(data)

            self.prod_obj = PostProduct.get_all_products(self)
            for product in self.prod_obj:
                return make_response(jsonify({
                    'Status': 'Ok',
                    'Message': "Product created Successfully",
                    'My Products': product
                }), 201)


class SingleProduct(Resource):
    # Get a single product
    @token_required
    def get(current_user, self, productID):
        self.prod_obj = PostProduct.get_all_products(self)
        if current_user:
            for product in self.prod_obj:
                if product['product_id'] == int(productID):
                    return make_response(jsonify({
                        'Status': 'Ok',
                        'Message': "Success",
                        'My product': product
                    }), 200)

            return make_response(jsonify({
                'Status': 'Failed',
                'Message': "No such product"
            }), 404)
        return make_response(jsonify({
            'Status': 'Failed',
            'Message': "You must be logged in first"
        }), 401)

    @token_required
    def put(current_user, self, productID):
        self.product_Id = int(productID)
        data = request.get_json()
        if current_user and current_user['role'] != "admin":
            return make_response(jsonify({
                'Status': 'Failed',
                'Message': "You must be an admin"
            }), 401)
        if current_user and current_user['role'] == "admin":
            valid_product = ValidateProduct(data)
            valid_product.validate_product_details()
            product = PostProduct()
            product.update_product(data, self.product_Id)

            self.prod_obj = PostProduct.get_all_products(self)
            for product in self.prod_obj:
                return make_response(jsonify({
                    'Status': 'Ok',
                    'Message': "Product updated Successfully",
                    'My Products': product
                }), 201)
