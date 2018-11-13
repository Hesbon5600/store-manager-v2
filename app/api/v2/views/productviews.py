'''Handles all functionality of routing product requests'''
from flask import jsonify, make_response, request
from flask_restful import Resource
from flask_expects_json import expects_json
from .expected_json import PRODUCT_JSON
from ..utils.productutils import ValidateProduct
from ..models.productmodels import PostProduct
from .tokenrequired import token_required
from .restrict import Restrict
from .productinput import ProductInput


class Product(Resource):
    '''Deals with posting a product and\
    returning the products from db'''

    def __init__(self):
        restrict = Restrict()
        self.admin_only = restrict.admin_only
        self.login_first = restrict.login_first
        self.no_such_product = restrict.no_such_product
    # Get all products

    @token_required
    def get(current_user, self):
        '''Function to return the saved users from the database'''
        self.prod_obj = PostProduct.get_all_products(self)
        if not current_user:
            response = self.login_first
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
            return self.admin_only
        valid_product = ValidateProduct(data)
        valid_product.validate_product_data_types()
        valid_product.validate_product_values()
        valid_product.validate_duplicates()
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

    def __init__(self):
        restrict = Restrict()
        self.admin_only = restrict.admin_only
        self.login_first = restrict.login_first
        self.no_such_product = restrict.no_such_product

    @token_required
    def get(current_user, self, product_id):
        '''Given the product ID select a\
        product that matches it from the DB'''
        self.prod_obj = PostProduct.get_all_products(self)
        if not current_user:
            return self.login_first
        for product in self.prod_obj:
            if product['product_id'] == int(product_id):
                return make_response(jsonify({
                    'Status': 'Ok',
                    'message': "Successfully fetched one product",
                    'Product': product
                }), 200)

        return self.no_such_product

    @token_required
    @expects_json(PRODUCT_JSON)
    def put(current_user, self, product_id):
        '''Update a specific product details'''
        self.product_Id = int(product_id)
        data = request.get_json()
        if current_user and current_user['role'] != "admin":
            return self.admin_only
        if current_user and current_user['role'] == "admin":
            valid_product = ValidateProduct(data)
            valid_product.validate_product_data_types()
            valid_product.validate_product_values()
            self.prod_obj = PostProduct.get_all_products(self)
            for product in self.prod_obj:
                if int(product['product_id']) != int(product_id)\
                        and product['title'].lower() == data['title'].lower():
                    message = "Product: '" + \
                        product['title'] + "' already exists"
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
                                'Product': product
                            }), 201)
            return self.no_such_product

    @token_required
    def delete(current_user, self, product_id):
        '''Delete a specific product'''
        self.product_Id = int(product_id)
        if current_user and current_user['role'] != "admin":
            return self.admin_only
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
            return self.no_such_product
