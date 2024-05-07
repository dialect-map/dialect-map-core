# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timezone

import pytest

from src.dialect_map_core.controllers import PaperController
from src.dialect_map_core.controllers import PaperAuthorController
from src.dialect_map_core.controllers import PaperReferenceCountersController
from src.dialect_map_core.models import Paper
from src.dialect_map_core.models import PaperAuthor
from src.dialect_map_core.models import PaperReferenceCounters
from src.dialect_map_core.storage import BaseDatabase
from src.dialect_map_core.storage import BaseDatabaseSession


@pytest.mark.usefixtures("rollback")
@pytest.mark.usefixtures("session")
class TestPaperController:
    """Class to group all the Paper model controller tests"""

    @pytest.fixture(scope="class")
    def controller(self, session: BaseDatabaseSession):
        """
        Creates a memory-based controller for the Paper records
        :param session: database session instance
        :return: initiated controller instance
        """

        return PaperController(session)

    def test_get(self, controller: PaperController):
        """
        Tests the retrieval of a paper revision by the controller
        :param controller: initiated instance
        """

        paper_id = "paper-01234"
        paper_obj = controller.get(paper_id, 1)

        assert type(paper_obj) is Paper
        assert paper_obj.id == paper_id

    def test_create(self, controller: PaperController):
        """
        Tests the creation of a paper by the controller
        :param controller: initiated instance
        """

        paper_id = "paper-creation"
        paper_rev = 1
        paper = Paper(
            arxiv_id=paper_id,
            arxiv_rev=paper_rev,
            title="Test Paper",
            submission_date=datetime.today().date(),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        creation_id = controller.create(paper)
        created_obj = controller.get(paper_id, paper_rev)

        assert creation_id == paper_id
        assert created_obj == paper

    def test_delete(self, controller: PaperController):
        """
        Tests the deletion of a paper by the controller
        :param controller: initiated instance
        """

        paper_id = "paper-deletion"
        paper_rev = 1
        paper = Paper(
            arxiv_id=paper_id,
            arxiv_rev=paper_rev,
            title="Test Paper",
            submission_date=datetime.today().date(),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        creation_id = controller.create(paper)
        deletion_id = controller.delete(paper_id)

        assert creation_id == deletion_id
        assert pytest.raises(ValueError, controller.get, paper_id, paper_rev)

    def test_delete_rev(self, controller: PaperController):
        """
        Tests the deletion of a paper revision by the controller
        :param controller: initiated instance
        """

        paper_id = "paper-deletion-rev"
        paper_rev = 1
        paper = Paper(
            arxiv_id=paper_id,
            arxiv_rev=paper_rev,
            title="Test Paper",
            submission_date=datetime.today().date(),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        controller.create(paper)
        deletion_id, deletion_rev = controller.delete_rev(paper_id, paper_rev)

        assert deletion_id == paper_id
        assert deletion_rev == paper_rev
        assert pytest.raises(ValueError, controller.get, paper_id, paper_rev)


@pytest.mark.usefixtures("rollback")
@pytest.mark.usefixtures("session")
class TestPaperAuthorController:
    """Class to group all the PaperAuthor model controller tests"""

    @pytest.fixture(scope="class")
    def controller(self, session: BaseDatabaseSession):
        """
        Creates a memory-based controller for the PaperAuthor records
        :param session: database session instance
        :return: initiated controller instance
        """

        return PaperAuthorController(session)

    def test_get(self, controller: PaperAuthorController):
        """
        Tests the retrieval of a paper author by the controller
        :param controller: initiated instance
        """

        all_authors = controller.get_by_paper("paper-01234", 1)
        one_author = all_authors[0]

        assert type(all_authors) is list
        assert type(one_author) is PaperAuthor
        assert one_author.id == "paper-author-01234-A"

    def test_create_with_non_existent_paper(
        self,
        database: BaseDatabase,
        controller: PaperAuthorController,
    ):
        """
        Tests the creation of a paper author by the controller
        when the referenced paper does not exist
        :param database: dummy database instance
        :param controller: initiated instance
        """

        author = PaperAuthor(
            arxiv_id="non-existing-paper",
            arxiv_rev=1,
            author_name="John Doe",
            created_at=datetime.now(timezone.utc),
        )

        assert pytest.raises(database.error, controller.create, author)


@pytest.mark.usefixtures("rollback")
@pytest.mark.usefixtures("session")
class TestPaperRefCounterController:
    """Class to group all the PaperReferenceCounter model controller tests"""

    @pytest.fixture(scope="class")
    def controller(self, session: BaseDatabaseSession):
        """
        Creates a memory-based controller for the PaperReferenceCounter records
        :param session: database session instance
        :return: initiated controller instance
        """

        return PaperReferenceCountersController(session)

    def test_get(self, controller: PaperReferenceCountersController):
        """
        Tests the retrieval of a paper ref. counter by the controller
        :param controller: initiated instance
        """

        all_counters = controller.get_by_paper("paper-01234", 1)
        one_counter = all_counters[0]

        assert type(all_counters) is list
        assert type(one_counter) is PaperReferenceCounters
        assert one_counter.id == "paper-ref-counter-01234-A"

    def test_create_with_non_existent_paper(
        self,
        database: BaseDatabase,
        controller: PaperReferenceCountersController,
    ):
        """
        Tests the creation of a paper ref. counter by the controller
        when the referenced paper does not exist
        :param database: dummy database instance
        :param controller: initiated instance
        """

        counter = PaperReferenceCounters(
            arxiv_id="non-existing-paper",
            arxiv_rev=1,
            arxiv_ref_count=0,
            total_ref_count=0,
            created_at=datetime.now(timezone.utc),
        )

        assert pytest.raises(database.error, controller.create, counter)
