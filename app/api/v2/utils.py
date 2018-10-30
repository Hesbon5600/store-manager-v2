from validate_email import validate_email
import re
from flask import make_response, jsonify, abort
from .models import User, PostProduct


class ValidateUser(User):
    def __init__(self, data):
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.role = data['role']

    def validate_user_details(self):
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
            if self.username == user["username"]:
                message = "Username '" + self.username + "' already taken"
                abort(406, message)
        for user in self.user_obj:
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
    def __init__(self, data):
        self.title = data['title']
        self.category = data['category']
        self.description = data['description']
        self.quantity = data['quantity']
        self.price = data['price']
        self.lower_inventory = data['lower_inventory']

    def validate_duplicates(self):
        self.prod_obj = PostProduct.get_all_products(self)
        for product in self.prod_obj:
            if product['title'] == self.title:
                message = "Product: '" + self.title + "' already exists"
                abort(406, message)

    def validate_product_details(self):

        if type(self.title) != str:
            message = "Product title must be a string"
            abort(400, message)

        if type(self.category) != str:
            message = "Product Category must be a string"
            abort(400, message)

        if type(self.description) != str:
            message = "Product Description must be a string"
            abort(400, message)

        if type(self.quantity) != int:
            message = "Product quantity price must be a real number"
            abort(400, message)
        if self.quantity < 0:
            message = "Product Quantity should be a positive value value"
            abort(400, message)

        if type(self.price) != float:
            message = "Product price must be of the format 00.00"
            abort(400, message)
        if self.price < 0:
            message = "Product price should be a positive value"
            abort(400, message)

        if type(self.lower_inventory) != int:
            message = "Product lower inventory must be a real number"
            abort(400, message)
        if self.lower_inventory < 0:
            message = "Product price should be a positive value"
            abort(400, message)
        if self.lower_inventory > self.quantity:
            message = "Lower inventory should be less than the quantity"
            abort(400, message)
