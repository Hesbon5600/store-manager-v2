from functools import wraps
from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api
from instance.config import Config
import jwt
from .models import *
from .utils import *
from werkzeug.security import check_password_hash
import datetime
import os


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
                token, Config.SECRET_KEY, algorithms=['HS256'])

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

