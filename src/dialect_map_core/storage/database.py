# -*- coding: utf-8 -*-

import logging
import time

from abc import ABC
from abc import abstractmethod
from typing import Type
from typing import Union

from sqlalchemy.engine import Connection
from sqlalchemy.engine import Transaction
from sqlalchemy.engine import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from .loader import BaseFileLoader
from .loader import JSONFileLoader
from ..models import Base


logger = logging.getLogger()


# Alias type definitions
SQLAlchemySession = Session
SQLAlchemyTransaction = Transaction

# Base type definitions
BaseDatabaseError = Union[SQLAlchemyError]
BaseDatabaseSession = Union[SQLAlchemySession]
BaseDatabaseTransaction = Union[SQLAlchemyTransaction]


class BaseDatabase(ABC):
    """Interface for the database classes"""

    @property
    @abstractmethod
    def error(self):
        """Database error type"""

        raise NotImplementedError()

    @abstractmethod
    def create_session(self):
        """
        Creates a database session object
        :return: scoped session or pure session
        """

        raise NotImplementedError()

    @abstractmethod
    def create_transaction(self):
        """
        Creates a database transaction object
        :return: database transaction object
        """

        raise NotImplementedError()

    @abstractmethod
    def close_connection(self):
        """Closes the database connection"""

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


class SQLDatabase(BaseDatabase):
    """Database class using SQLAlchemy utilities"""

    error = SQLAlchemyError

    def __init__(
        self,
        connection_url: str,
        backoff_seconds: int = 32,
        file_loader: BaseFileLoader | None = None,
    ):
        """
        Initiates the database connection
        :param connection_url: complete url to connect to the database
        :param backoff_seconds: maximum seconds to wait for connection (optional)
        :param file_loader: file loader to populate the database (optional)
        """

        if file_loader is None:
            file_loader = JSONFileLoader()

        logger.info(f"Connecting to database URL: {connection_url}")

        self.file_loader = file_loader
        self.max_backoff = backoff_seconds

        self.engine = create_engine(connection_url)
        self.connection = self._create_connection()
        self.session_factory = sessionmaker(bind=self.connection)

    def _create_connection(self) -> Connection:
        """
        Creates and returns a valid database connection.
        Performs exponential backoff upon connection failure.
        :return: Connection object
        """

        backoff_exp = 1
        backoff_secs = 2**backoff_exp

        while backoff_secs <= self.max_backoff:
            try:
                return self.engine.connect()
            except SQLAlchemyError:
                logger.info("Trying to connect to the database...")
                time.sleep(backoff_secs)
                backoff_exp += 1
                backoff_secs = 2**backoff_exp

        raise ConnectionError("Database connection timeout")

    def create_session(self) -> Session:
        """
        Creates a database session object
        :return: scoped session or pure session
        """

        return self.session_factory()

    def create_transaction(self) -> Transaction:
        """
        Creates a database transaction object
        :return: database transaction object
        """

        if self.connection.in_transaction():
            t = self.connection.get_transaction()
            t.close() if t else None

        return self.connection.begin()

    def close_connection(self):
        """Closes the database connection"""

        self.connection.close()

    def load(self, file_path: str, data_model: Type[Base]):
        """
        Loads a specific file of data objects into the database
        :param file_path: path to the specific file to load
        :param data_model: SQLAlchemy model to instantiate
        """

        logger.info(f"Loading {data_model.__name__} records")

        records = self.file_loader.load(file_path)
        objects = (data_model(**record) for record in records)

        with self.create_session() as session:
            session.add_all(objects)
            session.commit()

    def setup(self, check: bool = True):
        """
        Creates all the tables necessary to operate the project
        :param check: whether to respect the already created tables (optional)
        """

        with self.create_transaction():
            Base.metadata.create_all(bind=self.connection, checkfirst=check)

    def teardown(self, check: bool = False):
        """
        Deletes all project tables. Only useful when debugging
        :param check: whether to respect the filled tables (optional)
        """

        with self.create_transaction():
            Base.metadata.drop_all(bind=self.connection, checkfirst=check)
