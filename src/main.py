# -*- coding: utf-8 -*-

from flask import Flask
from config import ApplicationConfig
from config import EnvironmentConfigLoader
from globals import setup_service
from logs import setup_logger


app = Flask(__name__)


def setup_routes():
    """ Setup all the Flask blueprint routes """

    from routes import all_blueprints

    for bp in all_blueprints:
        app.register_blueprint(bp)


def setup_errors():
    """ Setup all the Flask exception handlers """

    from exceptions import not_found_request
    from exceptions import internal_error

    app.register_error_handler(ValueError, not_found_request)
    app.register_error_handler(Exception, internal_error)


# Gunicorn running the server
if __name__ == "main":

    loader = EnvironmentConfigLoader()
    config = ApplicationConfig(loader)

    # Setup order must be preserved
    setup_logger(config.log_level)
    setup_service(c=config)
    setup_routes()
    setup_errors()


# Flask running the server
if __name__ == "__main__":

    loader = EnvironmentConfigLoader()
    config = ApplicationConfig(loader)

    # Setup order must be preserved
    setup_logger(config.log_level)
    setup_service(c=config)
    setup_routes()
    setup_errors()
