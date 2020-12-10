# -*- coding: utf-8 -*-

import logging
from abc import ABCMeta
from abc import abstractmethod
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from typing import Type

from .loader import BaseFileLoader
from .loader import JSONFileLoader
from ..models.base import Base


logger = logging.getLogger()


class BaseDatabase(metaclass=ABCMeta):
    """ Interface for the database classes """

    @property
    @abstractmethod
    def engine(self):
        """ Database engine object """

        raise NotImplementedError()

    @property
    @abstractmethod
    def session(self):
        """ Database session object """

        raise NotImplementedError()

    @property
    @abstractmethod
    def session_error(self):
        """ Database highest error upon exception """

        raise NotImplementedError()

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

    engine = None
    session = None
    session_error = SQLAlchemyError

    def __init__(
        self,
        connection_url: str,
        factory_session: bool = True,
        files_loader: BaseFileLoader = None,
    ):
        """
        Initiates the database connection
        :param connection_url: complete url to connect to the database
        :param factory_session: whether to create a new session per request (optional)
        :param files_loader: file loader to populate the database if needed (optional)
        """

        if files_loader is None:
            files_loader = JSONFileLoader()

        logger.info(f"Connecting to database URL: {connection_url}")

        self.loader = files_loader
        self.web_app = factory_session
        self.engine = create_engine(connection_url)
        self.session = self.__init_session(self.web_app)

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
