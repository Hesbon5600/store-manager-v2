'''Registering the blueprint'''
from flask import Flask, Blueprint, make_response, jsonify
from instance.config import app_config
from .api.v2 import v2 as version2


def create_app(config_name="development"):
    app = Flask("__name__", instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    @app.errorhandler(404)
    def not_found(e):
        '''Defining a custom message for not found'''
        return make_response(jsonify({
            "Message": "What you are looking for\
            was Not found (The route is wrong)"
        }), 404)

    @app.errorhandler(500)
    def internal_error(error):
        '''Defining a custom message for internal server error'''
        return make_response(jsonify({
            "Message": "The system ran into a problem due to\
            an internal server error \n Consider fixing"
        }), 500)

    ''' Configure the app and registre blueprints '''

    app.register_blueprint(version2)
    return app
