# -*- coding: utf-8 -*-

import pytest
from controllers import CategoryController
from datetime import datetime
from models import Category
from storage import BaseDatabase


def test_category_get(db: BaseDatabase):
    """
    Tests the retrieval of a category using a controller
    :param db: initiated and loaded database
    """

    controller = CategoryController(db=db)
    category = controller.get("category-01234")

    assert type(category) is Category
    assert category.id == "category-01234"


def test_category_create(db: BaseDatabase):
    """
    Tests the creation of a category using a controller
    :param db: initiated and loaded database
    """

    controller = CategoryController(db=db)

    category_id = "category-creation"
    category_ds = "My test category"
    category = Category(
        category_id=category_id,
        description=category_ds,
        created_at=datetime.now(),
    )

    creation_id = controller.create(category)
    created_obj = controller.get(category_id)

    assert creation_id == category_id
    assert created_obj == category


def test_category_delete(db: BaseDatabase):
    """
    Tests the deletion of a category using a controller
    :param db: initiated and loaded database
    """

    controller = CategoryController(db=db)

    category_id = "category-deletion"
    category_ds = "My test category"
    category = Category(
        category_id=category_id,
        description=category_ds,
        created_at=datetime.now(),
    )

    creation_id = controller.create(category)
    deletion_id = controller.delete(category_id)

    assert creation_id == deletion_id

    with pytest.raises(ValueError):
        controller.get(category_id)
