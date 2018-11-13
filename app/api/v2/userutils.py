'''All the user validations are handled here'''
import re
from validate_email import validate_email
from flask import make_response, jsonify, abort
from .models.usermodels import User


class ValidateUser(User):
    ''' Class that handles validating users input '''

    def __init__(self, data):
        self.username = data['username'].strip()
        self.email = data['email'].strip()
        self.password = data['password'].strip()
        self.role = data['role'].strip()

    def validate_missing_user_details(self):
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

    def validate_duplicate_data(self):
        for user in self.user_obj:
            if self.username.lower() == user["username"].lower():
                message = "Username '" + self.username + "' already taken"
                abort(406, message)
            if self.email == user["email"]:
                message = "Email '" + self.email + "' already taken"
                abort(406, message)

    def validate_user_imput_types(self):
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

    def validate_password(self):
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