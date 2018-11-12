'''All the product validations are handled here'''
import re
from validate_email import validate_email
from flask import make_response, jsonify, abort
from .models.productmodels import PostProduct


class ValidateProduct(PostProduct):
    ''' Handles Product validation  '''
    def __init__(self, data):
        self.title = data['title']
        self.category = data['category']
        self.description = data['description']
        self.quantity = data['quantity']
        self.price = data['price']
        self.lower_inventory = data['lower_inventory']

    def validate_duplicates(self):
        '''Ensure no product shares a name with another product.'''
        '''Not called when updating a product'''
        self.prod_obj = PostProduct.get_all_products(self)
        for product in self.prod_obj:
            if product['title'].lower() == self.title.lower():
                message = "Product: '" + self.title + "' already exists"
                abort(406, message)

    def validate_product_details(self):
        '''More validations for the product'''
        try:
            price = float(self.price)
        except:
            message = "Product price must be of the format 00.00"
            abort(400, message)
        try:
            lower_inventory = int(self.lower_inventory)
        except:
            message = "Product Lower inventory must be whole number"
            abort(400, message)
        try:
            quantity = int(self.quantity)
        except:
            message = "Product quantity must be anumber"
            abort(400, message)

        if float(self.price) < 0:
            message = "Product price should be greater than 0"
            abort(400, message)
        if int(self.quantity) < 0:
            message = "Product Quantity should be a positive value value"
            abort(400, message)

        if int(self.lower_inventory) < 0:
            message = "Product price should be value greater than 0"
            abort(400, message)
        if int(self.lower_inventory) > int(self.quantity):
            message = "Lower inventory should be less than the quantity"
            abort(400, message)
