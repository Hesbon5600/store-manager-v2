from functools import wraps
import jwt
from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api
from flask_expects_json import expects_json
from instance.config import app_config
from .expected_json import *
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
    @expects_json(USER_REGISTRATION_JSON)
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
    @expects_json(USER_LOGIN_JSON)
    def post(self):
        self.user_obj = User.get_all_users(self)
        data = request.get_json()
        username = data['username'].strip()
        password = data['password'].strip()

        if not data or not username or not password or 'username' not in data or 'password' not in data:
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
                return make_response(jsonify({'Message': "Successfully logged in as '" + user['role'],
                                              'token': token.decode('UTF-8')
                                              }), 200)

        return make_response(jsonify({
            'Status': 'Failed',
            'Message': "No such user found. Check your login credentials"
        }), 404)


class PromoteUser(Resource):
    @token_required
    def put(current_user, self, user_id):
        self.user_id = int(user_id)
        self.user_obj = User.get_all_users(self)
        # data = request.get_json()
        if current_user and current_user['role'] != "admin":
            return make_response(jsonify({
                'Status': 'Failed',
                'Message': "You must be an admin"
            }), 401)
        for user in self.user_obj:
            if int(user['user_id']) != int(self.user_id):
                return make_response(jsonify({
                    'Status': 'Failed',
                    'Message': "No such user"
                }), 400)
                # print(user)
            if user['role'] == 'admin':
                return make_response(jsonify({
                    'Status': 'Failed',
                    'Message': "User '" + user['username'] + "' is already an admin"
                }), 400)
            update_user = User()
            update_user.update_user(self.user_id)
            return make_response(jsonify({
                'Status': 'Ok',
                'Message': "User '" + user['username'] + "' has been promoted to admin"
            }), 200)


class Product(Resource):
    # Get all products
    @token_required
    def get(current_user, self):
        self.prod_obj = PostProduct.get_all_products(self)
        if not current_user:
            response = make_response(jsonify({
                'Status': 'Failed',
                'Message': "You must first login"
            }), 401)
        if len(self.prod_obj) < 1:
            response = make_response(jsonify({
                'Status': 'Failed',
                'Message': "No avilable products"
            }), 404)
        else:
            response = make_response(jsonify({
                'Status': 'Ok',
                'Message': "Successfully fetched all products",
                'My products': self.prod_obj
            }), 200)

        return response

    @token_required
    @expects_json(PRODUCT_JSON)
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
                if product['title'] == data['title']:
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
        if not current_user:
            return make_response(jsonify({
                'Status': 'Failed',
                'Message': "You must be logged in first"
            }), 401)
        for product in self.prod_obj:
            if product['product_id'] == int(productID):
                return make_response(jsonify({
                    'Status': 'Ok',
                    'Message': "Successfully fetched one product",
                    'My product': product
                }), 200)

        return make_response(jsonify({
            'Status': 'Failed',
            'Message': "No such product"
        }), 404)

    @token_required
    @expects_json(PRODUCT_JSON)
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
            self.prod_obj = PostProduct.get_all_products(self)
            for product in self.prod_obj:
                if product['product_id'] != productID:
                    return make_response(jsonify({
                        'Status': 'Failed',
                        'Message': "No such product"
                    }), 404)
                product = PostProduct()
                product.update_product(data, self.product_Id)
                return make_response(jsonify({
                    'Status': 'Ok',
                    'Message': "Product updated Successfully",
                    'My Products': product
                }), 201)

    @token_required
    def delete(current_user, self, productID):
        self.product_Id = int(productID)
        data = request.get_json()
        if current_user and current_user['role'] != "admin":
            return make_response(jsonify({
                'Status': 'Failed',
                'Message': "You must be an admin"
            }), 401)
        if current_user and current_user['role'] == "admin":
            self.prod_obj = PostProduct.get_all_products(self)
            if len(self.prod_obj) > 0:
                for product in self.prod_obj:
                    if product['product_id'] == self.product_Id:
                        product = PostProduct()
                        product.delete_product(self.product_Id)
                        return make_response(jsonify({
                            'Status': 'Ok',
                            'Message': "Product deleted Successfully"
                        }), 200)
                return make_response(jsonify({
                    'Status': 'Failed',
                    'Message': "Product does nor exist",
                    'Avilable products': self.prod_obj
                }), 404)
            return make_response(jsonify({
                'Status': 'Failed',
                'Message': "No avilable products"
            }), 404)


class Sale(Resource):
    # Make a sales
    @token_required
    @expects_json(SALE_JSON)
    def post(current_user, self):
        total = 0
        data = request.get_json()
        if current_user and current_user['role'] != 'attendant':
            return make_response(jsonify({
                                         'Status': 'Failed',
                                         'Message': "You must be an attendant"
                                         }), 403)
        if not data or not data['product_title']:
            return make_response(jsonify({
                                         'Status': 'Failed',
                                         'Message': "No data posted"
                                         }), 400)
        product_title = data['product_title']
        product_quantity = data['product_quantity']
        # product_quantity
        self.prod_obj = PostProduct.get_all_products(self)
        for product in self.prod_obj:
            if product['title'] == data['product_title'] and int(product['quantity']) < 1:
                return make_response(jsonify({
                    'Status': 'Failed',
                    'Message': "No more products to sell"
                }), 404)

            if product['title'] == product_title:
                if product['quantity'] < product_quantity:
                    return make_response(jsonify({
                        'Status': 'Failed',
                        'Message': "You are attempting to sale more products than avilable"
                    }), 403)
                attendant_id = current_user['user_id']
                product_id = product['product_id']
                post_sale = PostSale()
                new_sale = {
                    "attendant_id": attendant_id,
                    "product_id": product_id,
                    "product_quantity": product_quantity
                }
                post_sale.save_sale(new_sale)
                product['quantity'] = product['quantity'] - product_quantity
                product_id = product_id
                update_prod = PostProduct()
                update_prod.update_sold_product(product, product_id)
                self.sale_obj = PostSale.get_all_sales(self)
                for sale in self.sale_obj:
                    if product['product_id'] in sale.values():
                        total = total + int(product['price'])
                return make_response(jsonify({
                    'Status': 'Ok',
                    'Message': "Sale made successfully",
                    'My Sales': product,
                    "Total": total
                }), 201)
        return make_response(jsonify({
            'Status': 'Failed',
            'Message': "product does not exist"
        }), 404)

    # Get all sale entries
    @token_required
    def get(current_user, self):
        if current_user and current_user['role'] != "admin":
            return make_response(jsonify({
            'Status': 'Failed',
            'Message': "You must be logged in as an admin"
        }), 403)
        self.sale_obj = PostSale.get_all_sales(self)
        if len(self.sale_obj) > 0:
            response = make_response(jsonify({
                'Status': 'Ok',
                'Message': "Success",
                'My Sales': self.sale_obj
            }), 200)
        else:
            response = make_response(jsonify({
                'Status': 'Failed',
                'Message': "No sales made"
            }), 404)
        return response

        


class SingleSale(Resource):
    @token_required
    def get(current_user, self, saleID):
        self.sale_obj = PostSale.get_all_sales(self)
        for sale in self.sale_obj:
            if current_user['user_id'] == sale['attendant_id'] or current_user['role'] == 'admin':
                if int(saleID) == sale['sale_id']:
                    response = make_response(jsonify({
                        'Status': 'Ok',
                        'Message': "Success",
                        'Sale': sale
                    }), 200)

                else:
                    response = make_response(jsonify({
                        'Status': 'Failed',
                        'Message': "No avilable sales"
                    }), 404)
                return response
            else:
                return make_response(jsonify({
                    'Status': 'Failed',
                    'Message': "You cannor access this sale record"
                }), 401)
