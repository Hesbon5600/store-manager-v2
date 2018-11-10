'''All the validations are handled here'''
import re
from validate_email import validate_email
from flask import make_response, jsonify, abort
from .models import User, PostProduct


class ValidateUser(User):
    ''' Class that handles validating users input '''
    def __init__(self, data):
        self.username = data['username'].strip()
        self.email = data['email'].strip()
        self.password = data['password'].strip()
        self.role = data['role'].strip()

    def validate_user_details(self):
        ''' Check the input and eturn a message if an error is thrown '''
        self.user_obj = User.get_all_users(self)
        if not validate_email(self.email):
            message = "Email is invalid"
            abort(400, message)
        if self.username == "":
            message = "Username is missing"
            abort(400, message)
        if self.email == "":
            message = "Email is missing"
            abort(400, message)
        if self.password == "":
            message = "Password is missing"
            abort(400, message)
        if self.role == "":
            message = "Role is missing"
            abort(400, message)
        for user in self.user_obj:
            if self.username.lower() == user["username"].lower():
                message = "Username '" + self.username + "' already taken"
                abort(406, message)
            if self.email == user["email"]:
                message = "Email '" + self.email + "' already taken"
                abort(406, message)
        if type(self.username) != str:
            message = "Username must be a string"
            abort(400, message)
        if type(self.email) != str:
            message = "Email must be a string"
            abort(400, message)
        if type(self.password) != str:
            message = "Password must be a string"
            abort(400, message)
        if type(self.role) != str:
            message = "Role must be a string"
            abort(400, message)
        if len(self.password) <= 6 or len(self.password) > 12:
            message = "Password must be at least 6 and at most 10 ch long"
            abort(400, message)
        elif not any(char.isdigit() for char in self.password):
            message = "Password must have a digit"
            abort(400, message)
        elif not any(char.isupper() for char in self.password):
            message = "Password must have an upper case character"
            abort(400, message)
        elif not any(char.islower() for char in self.password):
            message = "Password must have a lower case character"
            abort(400, message)
        elif not re.search("[#@$]", self.password):
            message = "Password must have one of the special charater [#@$]"
            abort(400, message)


class ValidateProduct():
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
        try:
            price = float(self.price)
        except:
            message = "Product price must be of the format 00.00"
            abort(400, message)
        try:
            lower_inventory = int(self.lower_inventory)
        except:
            message = "Product Lower inventory must be anumber"
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
