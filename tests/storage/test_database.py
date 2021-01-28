# -*- coding: utf-8 -*-

import pytest

from src.dialect_map.storage import SQLAlchemyDatabase


def test_connection_exception():
    """ Tests the raised exception of a failed connection """

    db_arguments = {
        "connection_url": "postgresql+psycopg2://example.com",
        "backoff_seconds": 1,
    }

    assert pytest.raises(ConnectionError, SQLAlchemyDatabase, **db_arguments)


def test_sql_tables_creation():
    """ Tests the correct creation of all the database tables """

    db = SQLAlchemyDatabase("sqlite:///:memory:")
    db.setup(False)


def test_sql_tables_deletion():
    """ Tests the correct deletion of all the database tables """

    db = SQLAlchemyDatabase("sqlite:///:memory:")
    db.teardown(True)
