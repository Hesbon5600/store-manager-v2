"""Registering the blueprint"""
from flask import Flask, Blueprint
from instance.config import app_config
from .api.v2 import v2 as version2
from flask_cors import CORS


def create_app(config_name="development"):
    # @app.errorhandler(404)
    # def not_found():
    #     return make_response(jsonify({
    #         "message": "Innvalid route. Please check it"
    #     }), 404)

    # @app.errorhandler(500)
    # def internal_server_error():
    #     return make_response(jsonify({
    #         "message": "The server encountered an internal error"
    #     }), 500)

    """Configure the app and registre blueprints"""
    app = Flask("__name__", instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")

    app.register_blueprint(version2)
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    return app
