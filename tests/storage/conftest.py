# -*- coding: utf-8 -*-

import pytest

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
    database.session.execute("PRAGMA foreign_keys=ON")

    return database
