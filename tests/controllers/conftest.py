# -*- coding: utf-8 -*-

import pytest
from parsers import DateParser
from parsers import DatetimeParser
from storage import SQLAlchemyDatabase
from storage import JsonLoader
from ..utils import FILES_MAPPINGS


@pytest.fixture(scope="package")
def db() -> SQLAlchemyDatabase:
    """ Creates a memory-based database to test database operations """

    loader = JsonLoader(
        [
            DateParser(),
            DatetimeParser(),
        ]
    )

    database = SQLAlchemyDatabase("sqlite:///:memory:", loader)
    database.setup()

    for file_map in FILES_MAPPINGS:
        database.load(
            file_path=file_map["file"],
            data_model=file_map["model"],
        )

    return database
