# -*- coding: utf-8 -*-

import pytest

from src.dialect_map.storage import BaseDatabase
from src.dialect_map.storage import BaseDatabaseContext
from src.dialect_map.storage import JSONFileLoader
from src.dialect_map.storage import SQLAlchemyDatabase
from src.dialect_map.storage import SQLDatabaseContext
from src.dialect_map_data import FILES_MAPPINGS


@pytest.fixture(scope="package")
def database() -> SQLAlchemyDatabase:
    """
    Creates a memory-based database to test database operations
    :return: memory-based database object
    """

    loader = JSONFileLoader()
    database = SQLAlchemyDatabase("sqlite:///:memory:", file_loader=loader)

    ### NOTE:
    ### SQLite does not check foreign key integrity by default
    ### Ref: https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#foreign-key-support
    with database.create_session() as session:
        session.execute("PRAGMA foreign_keys=ON")

    return database


@pytest.fixture(scope="package")
def context(database: BaseDatabase):
    """
    Creates a database context to be used as test helper
    :param database: database to be used during the tests
    """

    context = SQLDatabaseContext(database)

    with context.tables():
        _ = [database.load(mapping.file, mapping.model) for mapping in FILES_MAPPINGS]
        yield context


@pytest.fixture(scope="function")
def database_rollback(context: BaseDatabaseContext):
    """
    Wraps a controller class test in order to roll back any DB operations.
    It is equivalent to the combination of unit-test 'setUp' and 'tearDown' methods.
    https://docs.sqlalchemy.org/en/14/orm/session_transaction.html (last section)
    """

    with context.transaction(commit=False):
        yield
