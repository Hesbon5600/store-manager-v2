
'''Handles all functionality of routing requests'''
from functools import wraps
import jwt
from flask import Flask, jsonify, make_response, request
from flask_restful import Resource
from werkzeug.security import check_password_hash
from flask_expects_json import expects_json

from instance.config import app_config
from .expected_json import *
from .models import *
from .utils import *
import datetime


def token_required(func):
    '''Define a wrapper that handles decoding of the token'''
    '''Identifies the user whom the token belongs to'''
    @wraps(func)
    def decorated(*args, **kwargs):
        user_obj = User()
        users = user_obj.get_all_users()

        token = None
        current_user = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        invalid_token = user_obj.get_invalid_tokens(token)
        if invalid_token:
            return make_response(jsonify({
                'message': 'You are logged out You must login again'
            }), 401)
        print(invalid_token)
        try:
            data = jwt.decode(
                token, app_config['development'].SECRET_KEY,
                algorithms=['HS256'])

            for user in users:
                if user['username'] == data['username']:
                    current_user = user
        except:
            return make_response(jsonify({'message': 'Token is invalid'}),
                                 403)
        return func(current_user, *args, **kwargs)
    return decorated


class UserRegistration(Resource):
    '''Handles user registration'''
    @expects_json(USER_REGISTRATION_JSON)
    def post(self):
        '''Get data from the user, call validation method'''
        '''pass the data to the User class for saving'''
        data = request.get_json()
        if not data:
            return make_response(jsonify({
                'Status': 'Failed',
                'message': "No signup data provided"
            }), 400)

        validate = ValidateUser(data)
        validate.validate_user_details()
        user = User(data)
        user.save_user()
        self.user_obj = User.get_all_users(self)
        for user in self.user_obj:
            if user['username'] == data['username']:
                return make_response(jsonify({
                    'Status': 'Ok',
                    'message': "User '" + user['username'] +
                    "' successfully registered as '" + user['role'],
                }), 201)


class UserLogin(Resource):
    '''Registered users can login'''
    @expects_json(USER_LOGIN_JSON)
    def post(self):
        '''User provides username and password'''
        self.user_obj = User.get_all_users(self)
        data = request.get_json()
        username = data['username'].strip()
        password = data['password'].strip()

        if not data or not username or not password or \
                'username' not in data or 'password' not in data:
            return make_response(jsonify({
                                         'Status': 'Failed',
                                         'message': "Please provide a username and password"
                                         }), 400)

        for user in self.user_obj:
            if user['username'] == username and\
                check_password_hash(user["password"],
                                    password):
                token = jwt.encode(
                    {'username': user['username'],
                     'exp': datetime.datetime.utcnow() +
                     datetime.timedelta(minutes=3000)},
                    app_config['development'].SECRET_KEY, algorithm='HS256')
                return make_response(
                    jsonify(
                        {'message': "Successfully logged in",
                         'token': token.decode('UTF-8')
                         }), 200)

        return make_response(jsonify({
            'Status': 'Failed',
            'message': "Check your login credentials"
        }), 404)


class Logout(Resource):
    @token_required
    def post(current_user, self):
        if not current_user:
            return make_response(jsonify({
                'message': 'You are not logged in'
            }), 401)
        user_obj = User()
        users = user_obj.get_all_users()
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({
                'message': 'You are not logged in'
            }), 401)
        logout = User().logout(token)
        if logout:
            return make_response(jsonify({
                'message': 'You have logged out'
            }), 200)


class GetUsers(Resource):
    '''Get all users'''
    def get(self):
        '''Get all users from the database'''
        self.user_obj = User.get_all_users(self)
        return make_response(jsonify({
                'Status': 'Ok',
                'message': "Successfully fetched all users",
                'users': self.user_obj
            }), 200)


class PromoteUser(Resource):
    '''Make an attendant to be an admin'''
    @token_required
    def put(current_user, self, user_id):
        '''Takes the user_id and updates the role to admin'''
        '''The initial role must be an attendant'''
        self.user_id = int(user_id)
        self.user_obj = User.get_all_users(self)
        # data = request.get_json()
        if current_user and current_user['role'] != "admin":
            return make_response(jsonify({
                'Status': 'Failed',
                'message': "You must be an admin"
            }), 401)
        for user in self.user_obj:
            if int(user['user_id']) == int(self.user_id):
                if user['role'] == 'admin':
                    return make_response(jsonify({
                        'Status': 'Failed',
                        'message': "User '" + user['username'] + "' is already an admin"
                    }), 400)
                update_user = User()
                update_user.update_user(self.user_id)
                return make_response(
                    jsonify({
                        'Status': 'Ok',
                        'message': "User has been promoted to admin"
                    }), 200)
        return make_response(jsonify({
            'Status': 'Failed',
            'message': "No such user",
            'All users': self.user_obj
        }), 400)


class Product(Resource):
    '''Deals with posting a product and\
    returning the products from db'''
    # Get all products
    @token_required
    def get(current_user, self):
        '''Function to return the saved users from the database'''
        self.prod_obj = PostProduct.get_all_products(self)
        if not current_user:
            response = make_response(jsonify({
                'Status': 'Failed',
                'message': "You must first login"
            }), 401)
        if len(self.prod_obj) < 1:
            response = make_response(jsonify({
                'Status': 'Failed',
                'message': "No available products"
            }), 404)
        else:
            response = make_response(jsonify({
                'Status': 'Ok',
                'message': "Successfully fetched all products",
                'products': self.prod_obj
            }), 200)

        return response

    @token_required
    @expects_json(PRODUCT_JSON)
    def post(current_user, self):
        '''Take the product data and save it in a database'''
        data = request.get_json()
        if current_user and current_user['role'] != "admin":
            return make_response(jsonify({
                'Status': 'Failed',
                'message': "You must be an admin"
            }), 401)
        if current_user and current_user['role'] == "admin":
            valid_product = ValidateProduct(data)
            valid_product.validate_duplicates()
            valid_product.validate_product_details()
            product = PostProduct(data)
            product.save_product()

            self.prod_obj = PostProduct.get_all_products(self)
            for product in self.prod_obj:
                if product['title'] == data['title']:
                    return make_response(jsonify({
                        'Status': 'Ok',
                        'message': "Product created Successfully",
                        'My Products': product
                    }), 201)


class SingleProduct(Resource):
    '''Get a single product from the DB'''
    @token_required
    def get(current_user, self, product_id):
        '''Given the product ID select a\
        product that matches it from the DB'''
        self.prod_obj = PostProduct.get_all_products(self)
        if not current_user:
            return make_response(jsonify({
                'Status': 'Failed',
                'message': "You must be logged in first"
            }), 401)
        for product in self.prod_obj:
            if product['product_id'] == int(product_id):
                return make_response(jsonify({
                    'Status': 'Ok',
                    'message': "Successfully fetched one product",
                    'Product': product
                }), 200)

        return make_response(jsonify({
            'Status': 'Failed',
            'message': "No such product"
        }), 404)

    @token_required
    @expects_json(PRODUCT_JSON)
    def put(current_user, self, product_id):
        '''Update a specific product details'''
        self.product_Id = int(product_id)
        data = request.get_json()
        if current_user and current_user['role'] != "admin":
            return make_response(jsonify({
                'Status': 'Failed',
                'message': "You must be an admin"
            }), 401)
        if current_user and current_user['role'] == "admin":
            valid_product = ValidateProduct(data)
            valid_product.validate_product_details()
            self.prod_obj = PostProduct.get_all_products(self)
            for product in self.prod_obj:
                if int(product['product_id']) != int(product_id) and product['title'].lower() == data['title'].lower():
                    message = "Product: '" + product['title'] + "' already exists"
                    abort(406, message)
                if int(product['product_id']) == int(product_id):
                    new_prod = PostProduct(data)
                    new_prod.update_product(self.product_Id)
                    self.prod_obj = PostProduct.get_all_products(self)
                    for product in self.prod_obj:
                        if int(product['product_id']) == int(product_id):
                            return make_response(jsonify({
                                'Status': 'Ok',
                                'message': "Product updated Successfully",
                                'New Product': product
                            }), 201)
            return make_response(jsonify({
                'Status': 'Failed',
                'message': "No such product"
            }), 404)

    @token_required
    def delete(current_user, self, product_id):
        '''Delete a specific product'''
        self.product_Id = int(product_id)
        if current_user and current_user['role'] != "admin":
            return make_response(jsonify({
                'Status': 'Failed',
                'message': "You must be an admin"
            }), 401)
        if current_user and current_user['role'] == "admin":
            self.prod_obj = PostProduct.get_all_products(self)
            if len(self.prod_obj) < 1:
                return make_response(jsonify({
                    'Status': 'Failed',
                    'message': "No available products"
                }), 404)
            for product in self.prod_obj:
                if int(product['product_id']) == self.product_Id:
                    product = PostProduct()
                    product.delete_product(self.product_Id)
                    return make_response(jsonify({
                        'Status': 'Ok',
                        'message': "Product deleted Successfully"
                    }), 200)
            return make_response(jsonify({
                'Status': 'Failed',
                'message': "No such product"
            }), 404)


class Sale(Resource):
    '''Post and get sales'''
    @token_required
    @expects_json(SALE_JSON)
    def post(current_user, self):
        '''Attendant can make a sale'''
        total = 0
        data = request.get_json()
        if current_user and current_user['role'] != 'attendant':
            return make_response(jsonify({
                                         'Status': 'Failed',
                                         'message': "You must be an attendant"
                                         }), 403)
        product_title = data['product_title']
        product_quantity = int(data['product_quantity'])
        # product_quantity
        if int(product_quantity) < 0:
            return make_response(jsonify({
                        'Status': 'Failed',
                        'message': "Product quantity must be more than 0"
                    }), 403)
        self.prod_obj = PostProduct.get_all_products(self)
        for product in self.prod_obj:
            if product['title'].lower() == data['product_title'].lower() \
                    and int(product['quantity']) < 1:
                return make_response(jsonify({
                    'Status': 'Failed',
                    'message': "No more products to sell"
                }), 404)

            if product['title'].lower() == product_title:
                if int(product['quantity']) < int(product_quantity):
                    return make_response(jsonify({
                        'Status': 'Failed',
                        'message': "You are attempting to sale more products than available",
                        'Avilable products': product
                    }), 403)
                total = total + int(product['price']) * int(product_quantity)
                attendant_id = current_user['user_id']
                product_id = product['product_id']
                new_sale = {
                    "attendant_id": attendant_id,
                    "product_id": product_id,
                    "product_quantity": product_quantity
                }
                post_sale = PostSale(new_sale)
                post_sale.save_sale()
                product['quantity'] = int(product['quantity']) - int(product_quantity)
                product_id = product_id
                update_prod = PostProduct()
                update_prod.update_sold_product(product, product_id)
                self.sale_obj = PostSale.get_all_sales(self)
                for sale in self.sale_obj:
                    if product['product_id'] in sale.values():
                        return make_response(jsonify({
                            'Status': 'Ok',
                            'message': "Sale made successfully",
                            'Remaining products': product,
                            'Total': total
                        }), 201)
        return make_response(jsonify({
            'Status': 'Failed',
            'message': "product does not exist"
        }), 404)

    # Get all sale entries
    @token_required
    def get(current_user, self):
        '''Admin can get all sales'''
        if not current_user:
            return make_response(jsonify({
                'Status': 'Failed',
                'message': "You must be logged in first"
            }), 403)
        self.sale_obj = PostSale.get_all_sales(self)
        if len(self.sale_obj) > 0:
            response = make_response(jsonify({
                'Status': 'Ok',
                'message': "Success",
                'Sales': self.sale_obj
            }), 200)
        else:
            response = make_response(jsonify({
                'Status': 'Failed',
                'message': "No sales made"
            }), 404)
        return response


class SingleSale(Resource):
    '''Getting a single sale record'''
    @token_required
    def get(current_user, self, sale_id):
        '''Admin and the attendant who made the sale\
        Can view the sale record'''
        self.sale_obj = PostSale.get_all_sales(self)
        for sale in self.sale_obj:
            if current_user['role'] == 'admin' or current_user['user_id'] == sale['attendant_id']:
                if int(sale_id) == sale['sale_id']:
                    return make_response(jsonify({
                        'Status': 'Ok',
                        'message': "Success",
                        'Sale': sale
                    }), 200)
            else:
                return make_response(jsonify({
                    'Status': 'Failed',
                    'message': "You cannor access this sale record"
                }), 401)
        else:
            return make_response(jsonify({
                'Status': 'Failed',
                'message': "No such sale record"
            }), 404)
