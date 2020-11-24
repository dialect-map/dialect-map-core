# -*- coding: utf-8 -*-

import atexit
from config import ApplicationConfig
from service import ApplicationService
from storage import SQLAlchemyDatabase


service: ApplicationService


def setup_service(c: ApplicationConfig):
    """
    Setup the global application service
    :param c: global application configuration
    """

    global service

    engine = SQLAlchemyDatabase(c.database_url)
    service = ApplicationService(engine)

    # Register the service cleanup function upon exiting
    atexit.register(service.stop)
