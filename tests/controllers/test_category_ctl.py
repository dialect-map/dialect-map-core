# -*- coding: utf-8 -*-

import pytest
from datetime import datetime

from src.dialect_map.controllers import CategoryController
from src.dialect_map.models import Category
from src.dialect_map.storage import BaseDatabase


@pytest.mark.usefixtures("database_rollback")
class TestCategoryController:
    """Class to group all the Category model controller tests"""

    @pytest.fixture(scope="class")
    def controller(self, database: BaseDatabase):
        """
        Creates a memory-based controller for the Category records
        :param database: dummy database instance
        :return: initiated controller instance
        """

        return CategoryController(db=database)

    def test_get(self, controller: CategoryController):
        """
        Tests the retrieval of a category by the controller
        :param controller: initiated instance
        """

        category_id = "category-01234"
        category_obj = controller.get(category_id)

        assert type(category_obj) is Category
        assert category_obj.id == category_id

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
            created_at=datetime.utcnow(),
        )

        creation_id = controller.create(category)
        deletion_id = controller.delete(category_id)

        assert creation_id == deletion_id
        assert pytest.raises(ValueError, controller.get, category_id)
