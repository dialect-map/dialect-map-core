# -*- coding: utf-8 -*-

import pytest
from datetime import datetime

from src.dialect_map.controllers import MembershipController
from src.dialect_map.models import CategoryMembership
from src.dialect_map.storage import BaseDatabase


@pytest.mark.usefixtures("database_rollback")
class TestMembershipController:
    """Class to group all the CategoryMembership model controller tests"""

    @pytest.fixture(scope="class")
    def controller(self, database: BaseDatabase):
        """
        Creates a memory-based controller for the Membership records
        :param database: dummy database instance
        :return: initiated instance
        """

        return MembershipController(db=database)

    def test_get(self, controller: MembershipController):
        """
        Tests the retrieval of a category membership by the controller
        :param controller: initiated instance
        """

        membership_id = "membership-01234"
        membership_obj = controller.get(membership_id)

        assert type(membership_obj) is CategoryMembership
        assert membership_obj.id == membership_id

    def test_get_by_paper(self, controller: MembershipController):
        """
        Tests the retrieval of a category membership by the controller
        :param controller: initiated instance
        """

        memberships = controller.get_by_paper("paper-01234", 1)

        assert type(memberships) is list
        assert len(memberships) == 2

    def test_create(self, controller: MembershipController):
        """
        Tests the creation of a category membership by the controller
        :param controller: initiated instance
        """

        membership_id = "membership-creation"
        membership = CategoryMembership(
            membership_id=membership_id,
            arxiv_id="paper-01234",
            arxiv_rev=2,
            category_id="category-01234",
            created_at=datetime.utcnow(),
        )

        creation_id = controller.create(membership)
        created_obj = controller.get(membership_id)

        assert creation_id == membership_id
        assert created_obj == membership

    def test_delete(self, controller: MembershipController):
        """
        Tests the deletion of a category membership by the controller
        :param controller: initiated instance
        """

        membership_id = "membership-deletion"
        membership = CategoryMembership(
            membership_id=membership_id,
            arxiv_id="paper-01234",
            arxiv_rev=2,
            category_id="category-01234",
            created_at=datetime.utcnow(),
        )

        creation_id = controller.create(membership)
        deletion_id = controller.delete(membership_id)

        assert creation_id == deletion_id
        assert pytest.raises(ValueError, controller.get, membership_id)
