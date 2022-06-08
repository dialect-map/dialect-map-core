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

    return database
