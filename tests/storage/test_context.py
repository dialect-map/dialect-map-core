# -*- coding: utf-8 -*-

from contextlib import suppress
from datetime import datetime
from datetime import timezone

import pytest

from src.dialect_map_core.controllers import CategoryController
from src.dialect_map_core.models import Category
from src.dialect_map_core.storage import BaseDatabase
from src.dialect_map_core.storage import BaseDatabaseContext
from src.dialect_map_core.storage import BaseDatabaseSession
from src.dialect_map_core.storage import SQLDatabaseContext


@pytest.mark.usefixtures("session")
class TestSQLDatabaseContext:
    """Class to group all the SQL database context tests"""

    @pytest.fixture(scope="class")
    def context(self, database: BaseDatabase):
        """
        Creates a database context to be used as test helper
        :param database: database to be used during the tests
        """

        return SQLDatabaseContext(database)

    def test_invalid_transaction(
        self,
        context: BaseDatabaseContext,
        session: BaseDatabaseSession,
    ):
        """
        Tests the rollback of record storage on invalid transactions
        :param context: database context instance
        :param session: database session instance
        """

        ctl = CategoryController(session=session)

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
        context: BaseDatabaseContext,
        session: BaseDatabaseSession,
    ):
        """
        Tests the storage of multiple records on committed marked transactions
        :param context: database context instance
        :param session: database session instance
        """

        ctl = CategoryController(session=session)

        with context.transaction(commit=True):
            ctl.create(
                Category(
                    category_id="example-1",
                    description="example",
                    archived=False,
                    created_at=datetime.now(timezone.utc),
                )
            )
            ctl.create(
                Category(
                    category_id="example-2",
                    description="example",
                    archived=False,
                    created_at=datetime.now(timezone.utc),
                )
            )

        assert type(ctl.get("example-1")) == Category
        assert type(ctl.get("example-2")) == Category

    def test_valid_transaction_uncommitted(
        self,
        context: BaseDatabaseContext,
        session: BaseDatabaseSession,
    ):
        """
        Tests the storage of multiple records on uncommitted marked transactions
        :param context: database context instance
        :param session: database session instance
        """

        ctl = CategoryController(session=session)

        with context.transaction(commit=False):
            ctl.create(
                Category(
                    category_id="example-3",
                    description="example",
                    archived=False,
                    created_at=datetime.now(timezone.utc),
                )
            )
            ctl.create(
                Category(
                    category_id="example-4",
                    description="example",
                    archived=False,
                    created_at=datetime.now(timezone.utc),
                )
            )

        assert pytest.raises(ValueError, ctl.get, "example-3")
        assert pytest.raises(ValueError, ctl.get, "example-4")
