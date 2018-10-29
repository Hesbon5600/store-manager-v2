from functools import wraps
from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api
from instance.config import app_config
import jwt
from .models import *
from .utils import *
from .models import User
from werkzeug.security import check_password_hash
import datetime


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        current_user = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({
                'Message': 'Token is missing, You must login first'
            }), 401)
        try:
            data = jwt.decode(token, app_config['development'].SECRET_KEY)
            for user in users:
                if user['username'] == data['username']:
                    current_user = user
        except:
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
