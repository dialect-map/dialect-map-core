# -*- coding: utf-8 -*-

import logging
from abc import ABCMeta
from abc import abstractmethod
from models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from typing import Type
from .loader import BaseLoader

logger = logging.getLogger()


class BaseDatabase(metaclass=ABCMeta):
    """ Interface for the database classes """

    engine = None
    session = None
    session_error = None

    @abstractmethod
    def close(self):
        """ Closes the database connection """

        raise NotImplementedError()

    @abstractmethod
    def load(self, file_path: str, data_model):
        """
        Loads a specific file of data objects into the database
        :param file_path: path to the specific file to load
        :param data_model: data model to instantiate with each record
        """

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

    def __init__(self, connection_url: str, loader: BaseLoader, web_app: bool = False):
        """
        Initiates the database connection
        :param connection_url: complete url to connect to the database
        :param loader: file loader to populate the database if needed
        :param web_app: whether or not should be a new session per request
        """

        self.loader = loader
        self.web_app = web_app

        logger.info(f"Connecting to database URL: {connection_url}")
        self.engine = create_engine(connection_url)
        self.session = self.__init_session(web_app)
        self.session_error = SQLAlchemyError

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

        logger.info("Disconnecting from the database")

        if self.web_app:
            self.session.close()

    def load(self, file_path: str, data_model: Type):
        """
        Loads a specific file of data objects into the database
        :param file_path: path to the specific file to load
        :param data_model: SQLAlchemy model to instantiate
        """

        records = self.loader.load(file_path)

        for record in records:
            obj = data_model(**record)
            self.session.add(obj)  # type: ignore

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
