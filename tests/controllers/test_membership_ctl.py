# -*- coding: utf-8 -*-

import pytest
from datetime import datetime
from src.dialect_map.controllers import MembershipController
from src.dialect_map.models import CategoryMembership
from src.dialect_map.storage import BaseDatabase


def test_membership_get(db: BaseDatabase):
    """
    Tests the retrieval of a category membership using a controller
    :param db: initiated and loaded database
    """

    controller = MembershipController(db=db)
    membership = controller.get("membership-01234")

    assert type(membership) is CategoryMembership
    assert membership.id == "membership-01234"


def test_membership_create(db: BaseDatabase):
    """
    Tests the creation of a category membership using a controller
    :param db: initiated and loaded database
    """

    controller = MembershipController(db=db)

    membership_id = "membership-creation"
    membership = CategoryMembership(
        membership_id=membership_id,
        arxiv_id="paper-01234",
        arxiv_rev=1,
        category_id="category-01234",
        created_at=datetime.now(),
    )

    creation_id = controller.create(membership)
    created_obj = controller.get(membership_id)

    assert creation_id == membership_id
    assert created_obj == membership


def test_membership_delete(db: BaseDatabase):
    """
    Tests the deletion of a category membership using a controller
    :param db: initiated and loaded database
    """

    controller = MembershipController(db=db)

    membership_id = "membership-deletion"
    membership = CategoryMembership(
        membership_id=membership_id,
        arxiv_id="paper-01234",
        arxiv_rev=1,
        category_id="category-01234",
        created_at=datetime.now(),
    )

    creation_id = controller.create(membership)
    deletion_id = controller.delete(membership_id)

    assert creation_id == deletion_id

    with pytest.raises(ValueError):
        controller.get(membership_id)
