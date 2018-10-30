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
    def post(current_user, self):
        total = 0
        data = request.get_json()
        print(current_user)
        if not data or not data['product_id']:
            return make_response(jsonify({
                                         'Status': 'Failed',
                                         'Message': "No data posted"
                                         }), 400)
        product_id = data['product_id']
        if current_user and current_user['role'] == 'attendant':
            self.prod_obj = PostProduct.get_all_products(self)
            for product in self.prod_obj:
                if int(product['quantity']) > 0:
                    if product['product_id'] == product_id:
                        attendant_id = current_user['user_id']
                        post_sale = PostSale()
                        post_sale.save_sale(attendant_id, product_id)
                        product['quantity'] = product['quantity'] - 1
                        productId = product_id
                        update_prod = PostProduct()
                        update_prod.update_product(product, productId)
                        self.sale_obj = PostSale.get_all_sales(self)
                        for sale in self.sale_obj:
                            if product['product_id'] in sale.values():
                                total = total + int(product['price'])
                        return make_response(jsonify({
                            'Status': 'Ok',
                            'Message': "Success",
                            'My Sales': product,
                            "Total": total
                        }), 201)
                    else:
                        return make_response(jsonify({
                            'Status': 'Failed',
                            'Message': "product does not exist"
                        }), 404)
                else:
                    return make_response(jsonify({
                                         'Status': 'Failed',
                                         'Message': "No more products to sell"
                                         }), 404)
        else:
            return make_response(jsonify({
                                         'Status': 'Failed',
                                         'Message': "You must be an attendant"
                                         }), 403)

    # Get all sale entries
    @token_required
    def get(current_user, self):
        if current_user['role'] == "admin":
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

        return make_response(jsonify({
            'Status': 'Failed',
            'Message': "You must be an admin"
        }), 403)


