# -*- coding: utf-8 -*-

import logging
from abc import ABCMeta
from abc import abstractmethod
from models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger()


class BaseDatabase(metaclass=ABCMeta):
    """ Interface for the database classes """

    @abstractmethod
    def close(self):
        """ Closes the database connection """

        raise NotImplementedError()

    @abstractmethod
    def setup(self, check: bool):
        """
        Creates all the tables necessary to operate the project
        :param check: whether to respect the already created tables
        """

        raise NotImplementedError()

    @abstractmethod
    def teardown(self, check: bool):
        """
        Deletes all project tables. Only useful when debugging
        :param check: whether to respect the filled tables
        """

        raise NotImplementedError()


class SQLAlchemyDatabase(BaseDatabase):
    """ Database class using SQLAlchemy utilities"""

    def __init__(self, connection_url: str, web_app: bool = False):
        """
        Initiates the database connection
        :param connection_url: complete url to connect to the database
        :param web_app: whether or not should be a new session per request
        """

        logger.info(f"Connecting to database URL: {connection_url}")

        self.engine = create_engine(connection_url)
        self.session = self.__init_session(web_app)
        self.web_app = web_app

    def __init_session(self, web_app: bool):
        """
        Initializes the database object session
        :param web_app: whether or not should be a new session per request
        :return: session or session factory
        """

        session = sessionmaker(bind=self.engine)

        if web_app:
            return scoped_session(session)
        else:
            return session()

    def close(self):
        """ Closes the database session """

        if self.web_app:
            self.session.close()

    def setup(self, check: bool = True):
        """
        Creates all the tables necessary to operate the project
        :param check: whether to respect the already created tables
        """

        Base.metadata.create_all(bind=self.engine, checkfirst=check)

    def teardown(self, check: bool = False):
        """
        Deletes all project tables. Only useful when debugging
        :param check: whether to respect the filled tables
        """

        Base.metadata.drop_all(bind=self.engine, checkfirst=check)
