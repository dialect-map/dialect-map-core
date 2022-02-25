# -*- coding: utf-8 -*-

from datetime import datetime

import pytest

from src.dialect_map.controllers import JargonController
from src.dialect_map.controllers import JargonGroupController
from src.dialect_map.models import Jargon
from src.dialect_map.models import JargonGroup
from src.dialect_map.storage import BaseDatabase


@pytest.mark.usefixtures("database_rollback")
class TestJargonController:
    """Class to group all the Jargon model controller tests"""

    @pytest.fixture(scope="class")
    def controller(self, database: BaseDatabase):
        """
        Creates a memory-based controller for the Jargon records
        :param database: dummy database instance
        :return: initiated controller instance
        """

        return JargonController(db=database)

    def test_get(self, controller: JargonController):
        """
        Tests the retrieval of a jargon by the controller
        :param controller: initiated instance
        """

        jargon_id = "jargon-01234"
        jargon_obj = controller.get(jargon_id)

        assert type(jargon_obj) is Jargon
        assert jargon_obj.id == jargon_id

    def test_get_archived(self, controller: JargonController):
        """
        Tests the raised error when retrieving an archived jargon
        :param controller: initiated instance
        """

        assert pytest.raises(ValueError, controller.get, "jargon-archived")

    def test_get_by_string(self, controller: JargonController):
        """
        Tests the retrieval of a jargon by the controller
        :param controller: initiated instance
        """

        jargon = controller.get_by_string("One string")

        assert type(jargon) is Jargon
        assert jargon.id == "jargon-01234"

    def test_get_by_group(self, controller: JargonController):
        """
        Tests the retrieval of a jargon by the controller
        :param controller: initiated instance
        """

        jargons = controller.get_by_group("jargon-group-01234")

        assert type(jargons) is list
        assert len(jargons) == 2

    def test_create(self, controller: JargonController):
        """
        Tests the creation of a jargon by the controller
        :param controller: initiated instance
        """

        jargon_id = "jargon-creation"
        jargon_term = "My test jargon"
        jargon_regex = "[Mm]y test jargon"
        jargon = Jargon(
            jargon_id=jargon_id,
            jargon_term=jargon_term,
            jargon_regex=jargon_regex,
            archived=False,
            created_at=datetime.utcnow(),
        )

        creation_id = controller.create(jargon)
        created_obj = controller.get(jargon_id)

        assert creation_id == jargon_id
        assert created_obj == jargon

    def test_delete(self, controller: JargonController):
        """
        Tests the deletion of a jargon by the controller
        :param controller: initiated instance
        """

        jargon_id = "jargon-deletion"
        jargon_term = "My test jargon"
        jargon_regex = "[Mm]y test jargon"
        jargon = Jargon(
            jargon_id=jargon_id,
            jargon_term=jargon_term,
            jargon_regex=jargon_regex,
            archived=False,
            created_at=datetime.utcnow(),
        )

        creation_id = controller.create(jargon)
        deletion_id = controller.delete(jargon_id)

        assert creation_id == deletion_id
        assert pytest.raises(ValueError, controller.get, jargon_id)

    def test_archive(self, controller: JargonController):
        """
        Tests the archival of a jargon by the controller
        :param controller: initiated instance
        """

        jargon_id = "jargon-01234"
        jargon_id = controller.archive(jargon_id)
        jargon_obj = controller.get(jargon_id, include_archived=True)

        assert jargon_obj.archived is True
        assert jargon_obj.archived_at is not None


@pytest.mark.usefixtures("database_rollback")
class TestJargonGroupController:
    """Class to group all the JargonGroup model controller tests"""

    @pytest.fixture(scope="class")
    def controller(self, database: BaseDatabase):
        """
        Creates a memory-based controller for the JargonGroup records
        :param database: dummy database instance
        :return: initiated controller instance
        """

        return JargonGroupController(db=database)

    def test_get(self, controller: JargonGroupController):
        """
        Tests the retrieval of a jargon group by the controller
        :param controller: initiated instance
        """

        group_id = "jargon-group-01234"
        group_obj = controller.get(group_id)

        assert type(group_obj) is JargonGroup
        assert group_obj.id == group_id

    def test_create(self, controller: JargonGroupController):
        """
        Tests the creation of a jargon group by the controller
        :param controller: initiated instance
        """

        group_id = "jargon-group-creation"
        group_ds = "My test group"
        group = JargonGroup(
            group_id=group_id,
            description=group_ds,
            archived=False,
            created_at=datetime.utcnow(),
        )

        creation_id = controller.create(group)
        created_obj = controller.get(group_id)

        assert creation_id == group_id
        assert created_obj == group

    def test_create_nested(self, database: BaseDatabase):
        """
        Tests the creation of a jargon group by the controller,
        when nested jargon records are passed to the constructor
        :param database: dummy database instance
        """

        group_id = "jargon-group-creation-nested"
        jargon_id = "jargon-creation-nested"

        group = JargonGroup(
            **{
                "group_id": group_id,
                "description": "My nested group",
                "archived": False,
                "created_at": datetime.utcnow(),
                "jargons": [
                    {
                        "group_id": group_id,
                        "jargon_id": jargon_id,
                        "jargon_term": "One string",
                        "jargon_regex": "[Oo]ne string",
                        "archived": False,
                        "created_at": datetime.utcnow(),
                    },
                ],
            }
        )

        group_controller = JargonGroupController(db=database)
        jargon_controller = JargonController(db=database)

        created_group_id = group_controller.create(group)
        created_group = group_controller.get(group_id)
        created_jargon = jargon_controller.get(jargon_id)

        assert created_group_id == group_id
        assert type(created_group) == JargonGroup
        assert type(created_jargon) == Jargon

    def test_delete(self, controller: JargonGroupController):
        """
        Tests the deletion of a jargon group by the controller
        :param controller: initiated instance
        """

        group_id = "jargon-group-deletion"
        group_ds = "My test group"
        group = JargonGroup(
            group_id=group_id,
            description=group_ds,
            archived=False,
            created_at=datetime.utcnow(),
        )

        creation_id = controller.create(group)
        deletion_id = controller.delete(group_id)

        assert creation_id == deletion_id
        assert pytest.raises(ValueError, controller.get, group_id)
