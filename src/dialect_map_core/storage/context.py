# -*- coding: utf-8 -*-

import logging

from abc import ABC
from abc import abstractmethod
from contextlib import contextmanager
from contextlib import AbstractContextManager
from typing import Generator

from .database import BaseDatabase


logger = logging.getLogger()


class BaseDatabaseContext(ABC):
    """Interface for the Database context classes"""

    @abstractmethod
    def tables(self, check: bool) -> AbstractContextManager:
        """
        Context manager to wrap operations within existing tables
        :param check: whether to check if wrap operations can be done safely
        """

        raise NotImplementedError()

    @abstractmethod
    def transaction(self, commit: bool) -> AbstractContextManager:
        """
        Context manager to wrap operations in a SQL transaction
        :param commit: whether to commit the operations at exit
        """

        raise NotImplementedError()


class SQLDatabaseContext(BaseDatabaseContext):
    """Database context class for the SQL type databases"""

    def __init__(self, db: BaseDatabase):
        """
        Initializes the context with the underlying database
        :param db: database engine to use
        """

        self.db = db

    @contextmanager
    def tables(self, check: bool = False) -> Generator:
        """
        Context manager to wrap operations within existing tables
        :param check: whether to check if wrap operations can be done safely (optional)
        """

        self.db.setup(check)

        try:
            yield
        finally:
            self.db.teardown(check)

    @contextmanager
    def transaction(self, commit: bool = True) -> Generator:
        """
        Context manager to wrap operations in a SQL transaction
        :param commit: whether to commit the operations at exit (optional)
        """

        transaction = self.db.create_transaction()

        try:
            yield
        except self.db.error as e:
            logger.error(f"Database operation failed: {e}.")
            logger.error(f"The transaction will not be committed")
            raise
        else:
            transaction.commit() if commit else None
        finally:
            transaction.close()
