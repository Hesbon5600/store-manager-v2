'''Handles all functionality of routing sale requests'''
import jwt
from flask import jsonify, make_response, request
from flask_restful import Resource
from werkzeug.security import check_password_hash
from flask_expects_json import expects_json
from .expected_json import USER_LOGIN_JSON, USER_REGISTRATION_JSON
from .userutils import ValidateUser
from .models.usermodels import User
import datetime
from instance.config import app_config
from .tokenrequired import token_required


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
                                         'message': "Please provide a\
                                         username and password"
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
                        'message': "User '" + user['username'] + "'\
                         is already an admin"
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
