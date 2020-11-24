# -*- coding: utf-8 -*-

from flask import Flask
from config import ApplicationConfig
from config import EnvironmentConfigLoader
from globals import setup_service
from logs import setup_logger


app = Flask(__name__)


def setup_routes():
    """ Setup all the Flask blueprint routes """

    from routes import blueprint_category
    from routes import blueprint_jargon
    from routes import blueprint_membership
    from routes import blueprint_paper
    from routes import blueprint_reference

    app.register_blueprint(blueprint_category)
    app.register_blueprint(blueprint_jargon)
    app.register_blueprint(blueprint_membership)
    app.register_blueprint(blueprint_paper)
    app.register_blueprint(blueprint_reference)


# Gunicorn running the server
if __name__ == "main":

    loader = EnvironmentConfigLoader()
    config = ApplicationConfig(loader)

    # Setup order must be preserved
    setup_logger(config.log_level)
    setup_service(c=config)
    setup_routes()


# Flask running the server
if __name__ == "__main__":

    loader = EnvironmentConfigLoader()
    config = ApplicationConfig(loader)

    # Setup order must be preserved
    setup_logger(config.log_level)
    setup_service(c=config)
    setup_routes()

    # Run the application
    app.run(host="0.0.0.0", port=8080, debug=False)
