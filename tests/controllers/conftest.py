# -*- coding: utf-8 -*-

import pytest
from src.dialect_map.storage import JSONFileLoader
from src.dialect_map.storage import SQLAlchemyDatabase
from ..utils import FILES_MAPPINGS


@pytest.fixture(scope="package")
def db() -> SQLAlchemyDatabase:
    """ Creates a memory-based database to test database operations """

    loader = JSONFileLoader()
    database = SQLAlchemyDatabase("sqlite:///:memory:", files_loader=loader)
    database.setup()

    for file_map in FILES_MAPPINGS:
        database.load(
            file_path=file_map["file"],
            data_model=file_map["model"],
        )

    return database
