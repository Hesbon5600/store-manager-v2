'''This module declared the common return messages\
for for validation'''
from flask import jsonify, make_response, request


class Restrict():
    ''''Declare the commor return messages'''
    def __init__(self):
        '''Initialize the response messages'''
        self.admin_only = make_response(jsonify({
            'Status': 'Failed',
            'message': "You must be an admin"
        }), 401)
        self.attendant_only = make_response(jsonify({
            'Status': 'Failed',
            'message': "You must be an attendant"
        }), 403)
        self.login_first = make_response(jsonify({
            'Status': 'Failed',
            'message': "You must be logged in first"
        }), 401)
        self.no_such_product = make_response(jsonify({
            'Status': 'Failed',
            'message': "No such product"
        }), 404)
