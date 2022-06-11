# -*- coding: utf-8 -*-

import pytest

from src.dialect_map.storage import BaseDatabase
from src.dialect_map.storage import BaseDatabaseSession
from src.dialect_map.storage import SQLAlchemyDatabase


@pytest.fixture(scope="package")
def database() -> SQLAlchemyDatabase:
    """
    Creates a memory-based database to test database operations
    :return: memory-based database object
    """

    database = SQLAlchemyDatabase("sqlite:///:memory:")
    database.setup(check=False)

    ### NOTE:
    ### SQLite does not check foreign key integrity by default
    ### Ref: https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#foreign-key-support
    with database.create_session() as session:
        session.execute("PRAGMA foreign_keys=ON")

    return database


@pytest.fixture(scope="function")
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
