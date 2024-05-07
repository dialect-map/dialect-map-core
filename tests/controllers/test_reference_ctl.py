# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timezone

import pytest

from src.dialect_map_core.controllers import ReferenceController
from src.dialect_map_core.models import PaperReference
from src.dialect_map_core.storage import BaseDatabase
from src.dialect_map_core.storage import BaseDatabaseSession


@pytest.mark.usefixtures("rollback")
@pytest.mark.usefixtures("session")
class TestPaperReferenceController:
    """Class to group all the PaperReference model controller tests"""

    @pytest.fixture(scope="class")
    def controller(self, session: BaseDatabaseSession):
        """
        Creates a memory-based controller for the PaperReference records
        :param session: database session instance
        :return: initiated controller instance
        """

        return ReferenceController(session)

    def test_get(self, controller: ReferenceController):
        """
        Tests the retrieval of a paper reference by the controller
        :param controller: initiated instance
        """

        reference_id = "reference-01234"
        reference_obj = controller.get(reference_id)

        assert type(reference_obj) is PaperReference
        assert reference_obj.id == reference_id

    def test_get_by_source(self, controller: ReferenceController):
        """
        Tests the retrieval of a paper reference by the source paper
        :param controller: initiated instance
        """

        paper_id = "paper-01234"
        paper_rev = 1

        all_refs = controller.get_by_source_paper(paper_id, paper_rev)
        one_ref = all_refs[0]

        assert type(all_refs) is list
        assert type(one_ref) is PaperReference
        assert one_ref.source_arxiv_id == paper_id
        assert one_ref.source_arxiv_rev == paper_rev

    def test_get_by_target(self, controller: ReferenceController):
        """
        Tests the retrieval of a paper reference by the target paper
        :param controller: initiated instance
        """

        paper_id = "paper-56789"
        paper_rev = 1

        all_refs = controller.get_by_target_paper(paper_id, paper_rev)
        one_ref = all_refs[0]

        assert type(all_refs) is list
        assert type(one_ref) is PaperReference
        assert one_ref.target_arxiv_id == paper_id
        assert one_ref.target_arxiv_rev == paper_rev

    def test_create(self, controller: ReferenceController):
        """
        Tests the creation of a paper reference by the controller
        :param controller: initiated instance
        """

        ref_id = "reference-creation"
        ref = PaperReference(
            reference_id=ref_id,
            source_arxiv_id="paper-01234",
            source_arxiv_rev=2,
            target_arxiv_id="paper-56789",
            target_arxiv_rev=2,
            created_at=datetime.now(timezone.utc),
        )

        creation_id = controller.create(ref)
        created_obj = controller.get(ref_id)

        assert creation_id == ref_id
        assert created_obj == ref

    def test_create_with_non_existent_source_paper(
        self,
        database: BaseDatabase,
        controller: ReferenceController,
    ):
        """
        Tests the creation of a paper reference by the controller
        when the referenced source paper does not exist
        :param database: dummy database instance
        :param controller: initiated instance
        """

        ref = PaperReference(
            source_arxiv_id="non-existing-paper",
            source_arxiv_rev=2,
            target_arxiv_id="paper-56789",
            target_arxiv_rev=2,
            created_at=datetime.now(timezone.utc),
        )

        assert pytest.raises(database.error, controller.create, ref)

    def test_create_with_non_existent_target_paper(
        self,
        database: BaseDatabase,
        controller: ReferenceController,
    ):
        """
        Tests the creation of a paper reference by the controller
        when the referenced target paper does not exist
        :param database: dummy database instance
        :param controller: initiated instance
        """

        ref = PaperReference(
            source_arxiv_id="paper-01234",
            source_arxiv_rev=2,
            target_arxiv_id="non-existing-paper",
            target_arxiv_rev=2,
            created_at=datetime.now(timezone.utc),
        )

        assert pytest.raises(database.error, controller.create, ref)

    def test_delete(self, controller: ReferenceController):
        """
        Tests the deletion of a paper reference by the controller
        :param controller: initiated instance
        """

        ref_id = "reference-deletion"
        ref = PaperReference(
            reference_id=ref_id,
            source_arxiv_id="paper-01234",
            source_arxiv_rev=2,
            target_arxiv_id="paper-56789",
            target_arxiv_rev=2,
            created_at=datetime.now(timezone.utc),
        )

        creation_id = controller.create(ref)
        deletion_id = controller.delete(ref_id)

        assert creation_id == deletion_id
        assert pytest.raises(ValueError, controller.get, ref_id)
