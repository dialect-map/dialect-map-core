# -*- coding: utf-8 -*-

from datetime import datetime

import pytest

from src.dialect_map_core.controllers import CategoryController
from src.dialect_map_core.models import Category
from src.dialect_map_core.storage import BaseDatabaseSession


@pytest.mark.usefixtures("rollback")
@pytest.mark.usefixtures("session")
class TestCategoryController:
    """Class to group all the Category model controller tests"""

    @pytest.fixture(scope="class")
    def controller(self, session: BaseDatabaseSession):
        """
        Creates a memory-based controller for the Category records
        :param session: database session instance
        :return: initiated controller instance
        """

        return CategoryController(session)

    def test_get(self, controller: CategoryController):
        """
        Tests the retrieval of a category by the controller
        :param controller: initiated instance
        """

        category_id = "category-01234"
        category_obj = controller.get(category_id)

        assert type(category_obj) is Category
        assert category_obj.id == category_id

    def test_get_all(self, controller: CategoryController):
        """
        Tests the retrieval of all categories by the controller
        :param controller: initiated instance
        """

        category_objs = controller.get_all()

        assert type(category_objs) is list
        assert len(category_objs) == 2

    def test_create(self, controller: CategoryController):
        """
        Tests the creation of a category by the controller
        :param controller: initiated instance
        """

        category_id = "category-creation"
        category_ds = "My test category"
        category = Category(
            category_id=category_id,
            description=category_ds,
            archived=False,
            created_at=datetime.utcnow(),
        )

        creation_id = controller.create(category)
        created_obj = controller.get(category_id)

        assert creation_id == category_id
        assert created_obj == category

    def test_delete(self, controller: CategoryController):
        """
        Tests the deletion of a category by the controller
        :param controller: initiated instance
        """

        category_id = "category-deletion"
        category_ds = "My test category"
        category = Category(
            category_id=category_id,
            description=category_ds,
            archived=False,
            created_at=datetime.utcnow(),
        )

        creation_id = controller.create(category)
        deletion_id = controller.delete(category_id)

        assert creation_id == deletion_id
        assert pytest.raises(ValueError, controller.get, category_id)
