# -*- coding: utf-8 -*-

import pytest
from datetime import datetime

from src.dialect_map.controllers import PaperController
from src.dialect_map.controllers import PaperAuthorController
from src.dialect_map.controllers import PaperReferenceCountersController
from src.dialect_map.models import Paper
from src.dialect_map.models import PaperAuthor
from src.dialect_map.models import PaperReferenceCounters
from src.dialect_map.storage import BaseDatabase


@pytest.mark.usefixtures("database_rollback")
class TestPaperController:
    """ Class to group all the Paper model controller tests """

    @pytest.fixture(scope="class")
    def controller(self, database: BaseDatabase):
        """
        Creates a memory-based controller for the Paper records
        :param database: dummy database instance
        :return: initiated controller instance
        """

        return PaperController(db=database)

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
            created_at=datetime.now(),
            updated_at=datetime.now(),
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
            created_at=datetime.now(),
            updated_at=datetime.now(),
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
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        controller.create(paper)
        deletion_id, deletion_rev = controller.delete_rev(paper_id, paper_rev)

        assert deletion_id == paper_id
        assert deletion_rev == paper_rev
        assert pytest.raises(ValueError, controller.get, paper_id, paper_rev)


@pytest.mark.usefixtures("database_rollback")
class TestPaperAuthorController:
    """ Class to group all the PaperAuthor model controller tests """

    @pytest.fixture(scope="class")
    def controller(self, database: BaseDatabase):
        """
        Creates a memory-based controller for the PaperAuthor records
        :param database: dummy database instance
        :return: initiated controller instance
        """

        return PaperAuthorController(db=database)

    def test_get(self, controller: PaperAuthorController):
        """
        Tests the retrieval of a paper author by the controller
        :param controller: initiated instance
        """

        all_authors = controller.get_by_paper("paper-01234", 1)
        one_author = all_authors[0]

        assert type(all_authors) == list
        assert type(one_author) is PaperAuthor
        assert one_author.id == "paper-author-01234-A"


@pytest.mark.usefixtures("database_rollback")
class TestPaperRefCounterController:
    """ Class to group all the PaperReferenceCounter model controller tests """

    @pytest.fixture(scope="class")
    def controller(self, database: BaseDatabase):
        """
        Creates a memory-based controller for the PaperReferenceCounter records
        :param database: dummy database instance
        :return: initiated controller instance
        """

        return PaperReferenceCountersController(db=database)

    def test_get(self, controller: PaperReferenceCountersController):
        """
        Tests the retrieval of a paper ref. counter by the controller
        :param controller: initiated instance
        """

        all_counters = controller.get_by_paper("paper-01234", 1)
        one_counter = all_counters[0]

        assert type(all_counters) == list
        assert type(one_counter) is PaperReferenceCounters
        assert one_counter.id == "paper-ref-counter-01234-A"
