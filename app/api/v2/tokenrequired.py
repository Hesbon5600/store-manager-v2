'''This module handles tokens'''
from instance.config import app_config
from flask import Flask, jsonify, make_response, request
from functools import wraps
import jwt
from .models.usermodels import User


def token_required(func):
    '''Define a wrapper that handles decoding of the token'''
    '''Identifies the user whom the token belongs to'''
    @wraps(func)
    def decorated(*args, **kwargs):
        user_obj = User()
        users = user_obj.get_all_users()

        token = None
        current_user = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        invalid_token = user_obj.get_invalid_tokens(token)
        if invalid_token:
            return make_response(jsonify({
                'message': 'You are logged out You must login again'
            }), 401)
        try:
            data = jwt.decode(
                token, app_config['development'].SECRET_KEY,
                algorithms=['HS256'])

            for user in users:
                if user['username'] == data['username']:
                    current_user = user
        except:
            return make_response(jsonify({'message': 'Token is invalid'}),
                                 403)
        return func(current_user, *args, **kwargs)
    return decorated
