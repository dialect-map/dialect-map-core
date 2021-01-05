# -*- coding: utf-8 -*-

import pytest

from src.dialect_map.storage import JSONFileLoader
from src.dialect_map.storage import SQLAlchemyDatabase
from src.dialect_map_data import FILES_MAPPINGS


@pytest.fixture(scope="package")
def db() -> SQLAlchemyDatabase:
    """
    Creates a memory-based database to test database operations
    :return: database object
    """

    loader = JSONFileLoader()
    database = SQLAlchemyDatabase("sqlite:///:memory:", files_loader=loader)
    database.setup()

    for mapping in FILES_MAPPINGS:
        database.load(
            file_path=mapping.file,
            data_model=mapping.model,
        )

    return database
