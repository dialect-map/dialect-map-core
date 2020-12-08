# -*- coding: utf-8 -*-

import pytest
from src.dialect_map.storage import BaseDatabase
from src.dialect_map.storage import SQLAlchemyDatabase


@pytest.fixture(scope="module")
def db() -> SQLAlchemyDatabase:
    """ Creates a dummy database to test database operations """

    return SQLAlchemyDatabase("sqlite:///:memory:")


def test_sql_table_creation(db: BaseDatabase):
    """
    Tests the correct creation of all the database tables.
    :param db: dummy database object
    """

    db.setup(False)


def test_dummy(db: BaseDatabase):
    """
    Tests the correct destruction of all the database tables.
    :param db: dummy database object
    """

    db.teardown(False)
