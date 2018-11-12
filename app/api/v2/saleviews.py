
'''Handles all functionality of routing sale requests'''
from flask import jsonify, make_response, request
from flask_restful import Resource
from flask_expects_json import expects_json
from .expected_json import SALE_JSON
from .models.salemodels import PostSale
from .models.productmodels import PostProduct
from .tokenrequired import token_required
from .restrict import Restrict


class Sale(Resource):
    '''Post and get sales'''

    def __init__(self):
        restrict = Restrict()
        self.admin_only = restrict.admin_only
        self.login_first = restrict.login_first
        self.no_such_product = restrict.no_such_product
        self.attendant_only = restrict.attendant_only

    @token_required
    @expects_json(SALE_JSON)
    def post(current_user, self):
        '''Attendant can make a sale'''
        total = 0
        data = request.get_json()
        if current_user and current_user['role'] != 'attendant':
            return self.attendant_only
        try:
            product_quantity = int(data['product_quantity'])
        except:
            return make_response(jsonify({
                                         'Status': 'Failed',
                                         'message': "You must enter\
                                          a product quantity"
                                         }), 403)

        product_title = data['product_title'].strip()
        product_quantity = int(data['product_quantity'])
        print(product_quantity)
        # product_quantity
        if int(product_quantity) < 1:
            return make_response(jsonify({
                'Status': 'Failed',
                'message': "Product quantity must be more than 0"
            }), 403)
        self.prod_obj = PostProduct.get_all_products(self)
        for product in self.prod_obj:
            print(product['title'].lower(), product_title.lower())
            if product['title'].lower() == product_title.lower() \
                    and int(product['quantity']) < 1:
                return make_response(jsonify({
                    'Status': 'Failed',
                    'message': "No more products to sell"
                }), 404)

            if product['title'].lower() == product_title.lower():
                if int(product['quantity']) < int(product_quantity):
                    return make_response(jsonify({
                        'Status': 'Failed',
                        'message': "You are attempting to sale \
                         more products than available",
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
                product['quantity'] = int(
                    product['quantity']) - int(product_quantity)
                product_id = product_id
                update_prod = PostProduct(product)
                update_prod.update_product(product_id)
                self.sale_obj = PostSale.get_all_sales(self)
                for sale in self.sale_obj:
                    if product['product_id'] in sale.values():
                        return make_response(jsonify({
                            'Status': 'Ok',
                            'message': "Sale made successfully",
                            'Remaining products': product,
                            'Total': total
                        }), 201)
        return self.no_such_product

    # Get all sale entries
    @token_required
    def get(current_user, self):
        '''Admin can get all sales'''
        if not current_user:
            return self.login_first
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
            if current_user['role'] == 'admin' or \
                    current_user['user_id'] == sale['attendant_id']:
                if int(sale_id) == sale['sale_id']:
                    return make_response(jsonify({
                        'Status': 'Ok',
                        'message': "Success",
                        'Sale': sale
                    }), 200)
            else:
                return make_response(jsonify({
                    'Status': 'Failed',
                    'message': "You cannot access this sale record"
                }), 401)
        else:
            return make_response(jsonify({
                'Status': 'Failed',
                'message': "No such sale record"
            }), 404)
