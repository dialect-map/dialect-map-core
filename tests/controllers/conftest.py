# -*- coding: utf-8 -*-

import pytest

from src.dialect_map_core.storage import BaseDatabase
from src.dialect_map_core.storage import BaseDatabaseContext
from src.dialect_map_core.storage import BaseDatabaseSession
from src.dialect_map_core.storage import JSONFileLoader
from src.dialect_map_core.storage import SQLDatabase
from src.dialect_map_core.storage import SQLDatabaseContext
from src.dialect_map_data import FILES_MAPPINGS


@pytest.fixture(scope="package")
def database() -> SQLDatabase:
    """
    Creates a memory-based database to test database operations
    :return: memory-based database object
    """

    loader = JSONFileLoader()
    database = SQLDatabase("sqlite:///:memory:", file_loader=loader)

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


@pytest.fixture(scope="class")
def rollback(context: BaseDatabaseContext):
    """
    Wraps a controller class test in order to roll back any DB operations.
    It is equivalent to the combination of unit-test 'setUp' and 'tearDown' methods.
    https://docs.sqlalchemy.org/en/14/orm/session_transaction.html (last section)
    """

    with context.transaction(commit=False):
        yield


@pytest.fixture(scope="class")
def session(database: BaseDatabase) -> BaseDatabaseSession:
    """
    Creates a database session object to be used during a single test
    :return: database session object
    """

    session = database.create_session()

    try:
        yield session
    finally:
        session.close()
