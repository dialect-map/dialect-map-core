# -*- coding: utf-8 -*-

from contextlib import suppress
from datetime import datetime

import pytest

from src.dialect_map.controllers import CategoryController
from src.dialect_map.models import Category
from src.dialect_map.storage import BaseDatabase
from src.dialect_map.storage import BaseDatabaseContext
from src.dialect_map.storage import SQLAlchemyDatabase
from src.dialect_map.storage import SQLDatabaseContext


class TestSQLDatabaseContext:
    """Class to group all the SQL database context tests"""

    @pytest.fixture(scope="class")
    def database(self):
        """
        Creates a memory-based database to test database operations
        :return: memory-based database object
        """

        database = SQLAlchemyDatabase("sqlite:///:memory:")
        database.setup(check=False)

        return database

    @pytest.fixture(scope="class")
    def context(self, database: BaseDatabase):
        """
        Creates a database context to be used as test helper
        :param database: database to be used during the tests
        """

        return SQLDatabaseContext(database)

    def test_invalid_transaction(self, database: BaseDatabase, context: BaseDatabaseContext):
        """
        Tests the rollback of record storage on invalid transactions
        :param database: database instance
        :param context: database context instance
        """

        ctl = CategoryController(db=database)

        with suppress(Exception):
            with context.transaction(commit=True):
                ctl.create(
                    Category(
                        category_id="example-0",
                        description="example",
                        archived=False,
                        created_at=None,
                    )
                )

        assert pytest.raises(ValueError, ctl.get, "example-0")

    def test_valid_transaction_committed(
        self,
        database: BaseDatabase,
        context: BaseDatabaseContext,
    ):
        """
        Tests the storage of multiple records on committed marked transactions
        :param database: database instance
        :param context: database context instance
        """

        ctl = CategoryController(db=database)

        with context.transaction(commit=True):
            ctl.create(
                Category(
                    category_id="example-1",
                    description="example",
                    archived=False,
                    created_at=datetime.utcnow(),
                )
            )
            ctl.create(
                Category(
                    category_id="example-2",
                    description="example",
                    archived=False,
                    created_at=datetime.utcnow(),
                )
            )

        assert type(ctl.get("example-1")) == Category
        assert type(ctl.get("example-2")) == Category

    @pytest.mark.skip(reason="Investigation needed")
    def test_valid_transaction_uncommitted(
        self,
        database: BaseDatabase,
        context: BaseDatabaseContext,
    ):
        """
        Tests the storage of multiple records on uncommitted marked transactions
        :param database: database instance
        :param context: database context instance
        """

        ctl = CategoryController(db=database)

        with context.transaction(commit=False):
            ctl.create(
                Category(
                    category_id="example-3",
                    description="example",
                    archived=False,
                    created_at=datetime.utcnow(),
                )
            )
            ctl.create(
                Category(
                    category_id="example-4",
                    description="example",
                    archived=False,
                    created_at=datetime.utcnow(),
                )
            )

        assert pytest.raises(ValueError, ctl.get, "example-3")
        assert pytest.raises(ValueError, ctl.get, "example-4")
