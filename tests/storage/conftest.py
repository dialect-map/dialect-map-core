# -*- coding: utf-8 -*-

import pytest

from sqlalchemy.sql import text

from src.dialect_map_core.storage import BaseDatabase
from src.dialect_map_core.storage import SQLDatabase


@pytest.fixture(scope="package")
def database() -> SQLDatabase:
    """
    Creates a memory-based database to test database operations
    :return: memory-based database object
    """

    database = SQLDatabase("sqlite:///:memory:")
    database.setup(check=False)

    ### NOTE:
    ### SQLite does not check foreign key integrity by default
    ### Ref: https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#foreign-key-support
    with database.create_session() as session:
        clause = text("PRAGMA foreign_keys=ON")
        session.execute(clause)

    return database


@pytest.fixture(scope="function")
def session(database: BaseDatabase):
    """
    Creates a database session object to be used during a single test
    :return: database session object
    """

    session = database.create_session()

    try:
        yield session
    finally:
        session.close()
