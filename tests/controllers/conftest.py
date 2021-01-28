# -*- coding: utf-8 -*-

import pytest

from src.dialect_map.controllers import BaseController
from src.dialect_map.storage import JSONFileLoader
from src.dialect_map.storage import SQLAlchemyDatabase
from src.dialect_map_data import FILES_MAPPINGS


@pytest.fixture(scope="package")
def database() -> SQLAlchemyDatabase:
    """
    Creates a memory-based database to test database operations
    :return: memory-based database object
    """

    loader = JSONFileLoader()
    database = SQLAlchemyDatabase("sqlite:///:memory:", file_loader=loader)
    database.setup()

    for mapping in FILES_MAPPINGS:
        database.load(
            file_path=mapping.file,
            data_model=mapping.model,
        )

    return database


@pytest.fixture(scope="function")
def database_rollback(controller: BaseController):
    """
    Wraps a controller class test in order to rollback any DB operation.
    It is equivalent to the combination of unit-test 'setUp' and 'tearDown' methods.
    Its implementation is based on the following SQLAlchemy documentation
    https://docs.sqlalchemy.org/en/13/orm/session_transaction.html (last section)
    """

    transaction = controller.db.conn.begin()
    yield
    controller.db.session.close()
    transaction.rollback()
