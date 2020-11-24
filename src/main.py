# -*- coding: utf-8 -*-

import atexit
from flask import Flask
from .config import ApplicationConfig
from .config import EnvironmentConfigLoader
from .logs import setup_logger
from .service import AppService
from .storage import SQLAlchemyDatabase


app = Flask(__name__)
service: AppService


def setup_service(c: ApplicationConfig) -> None:
    """
    Setup the global application service
    :param c: global application configuration
    """

    global service

    engine = SQLAlchemyDatabase(c.database_url)
    service = AppService(engine)

    # Register the service cleanup function upon exiting
    atexit.register(service.stop)


# Gunicorn running the server
if __name__ == "main":

    loader = EnvironmentConfigLoader()
    config = ApplicationConfig(loader)

    # Setup order must be preserved
    setup_logger(config.log_level)
    setup_service(c=config)


# Flask running the server
if __name__ == "__main__":

    loader = EnvironmentConfigLoader()
    config = ApplicationConfig(loader)

    # Setup order must be preserved
    setup_logger(config.log_level)
    setup_service(c=config)

    # Run the application
    app.run(host="0.0.0.0", port=8080, debug=False)
