# -*- coding: utf-8 -*-

import logging
import time

from abc import ABC
from abc import abstractmethod
from sqlalchemy.engine.base import Connection
from sqlalchemy.engine.create import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from typing import Type

from .loader import BaseFileLoader
from .loader import JSONFileLoader
from ..models.base import Base


logger = logging.getLogger()


class BaseDatabase(ABC):
    """Interface for the database classes"""

    @property
    @abstractmethod
    def conn(self):
        """Database connection object"""

        raise NotImplementedError()

    @property
    @abstractmethod
    def session(self):
        """Database session object"""

        raise NotImplementedError()

    @abstractmethod
    def close_conn(self):
        """Closes the database connection"""

        raise NotImplementedError()

    @abstractmethod
    def close_session(self):
        """Closes the database process / thread session"""

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
    """Database class using SQLAlchemy utilities"""

    conn = None
    session = None

    def __init__(
        self,
        connection_url: str,
        backoff_seconds: int = 32,
        thread_sessions: bool = True,
        file_loader: BaseFileLoader = None,
    ):
        """
        Initiates the database connection
        :param connection_url: complete url to connect to the database
        :param backoff_seconds: maximum seconds to wait for connection (optional)
        :param thread_sessions: whether or not to use thread-local sessions (optional)
        :param file_loader: file loader to populate the database if needed (optional)
        """

        if file_loader is None:
            file_loader = JSONFileLoader()

        logger.info(f"Connecting to database URL: {connection_url}")

        self.file_loader = file_loader
        self.max_backoff = backoff_seconds
        self.use_threads = thread_sessions

        self.engine = create_engine(connection_url)
        self.conn = self._create_connection()
        self.session = self._create_session()

    def _create_connection(self) -> Connection:
        """
        Creates and returns a valid database connection.
        Performs exponential backoff upon connection failure.
        :return: Connection object
        """

        backoff_exp = 1
        backoff_secs = 2 ** backoff_exp

        while backoff_secs <= self.max_backoff:
            try:
                return self.engine.connect()
            except SQLAlchemyError:
                logger.info("Trying to connect to the database...")
                time.sleep(backoff_secs)
                backoff_exp += 1
                backoff_secs = 2 ** backoff_exp

        raise ConnectionError("Database connection timeout")

    def _create_session(self):
        """
        Initializes the database object session
        :return: session factory or session registry
        """

        session = sessionmaker(bind=self.conn)

        if self.use_threads:
            return scoped_session(session)
        else:
            return session()

    def close_conn(self):
        """Closes the database connection"""

        self.conn.close()

    def close_session(self):
        """Closes the database session"""

        if self.use_threads:
            self.session.remove()
        else:
            self.session.close()

    def load(self, file_path: str, data_model: Type[Base]):
        """
        Loads a specific file of data objects into the database
        :param file_path: path to the specific file to load
        :param data_model: SQLAlchemy model to instantiate
        """

        records = self.file_loader.load(file_path)
        self.session.add_all(data_model(**record) for record in records)  # type: ignore
        self.session.commit()  # type: ignore

    def setup(self, check: bool = True):
        """
        Creates all the tables necessary to operate the project
        :param check: whether to respect the already created tables
        """

        Base.metadata.create_all(bind=self.conn, checkfirst=check)

    def teardown(self, check: bool = False):
        """
        Deletes all project tables. Only useful when debugging
        :param check: whether to respect the filled tables
        """

        Base.metadata.drop_all(bind=self.conn, checkfirst=check)
