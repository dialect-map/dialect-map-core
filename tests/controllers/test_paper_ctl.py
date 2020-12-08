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


def test_paper_get(db: BaseDatabase):
    """
    Tests the retrieval of a paper revision using a controller
    :param db: initiated and loaded database
    """

    controller = PaperController(db=db)
    paper = controller.get("paper-01234", 1)

    assert type(paper) is Paper
    assert paper.id == "paper-01234"


def test_paper_create(db: BaseDatabase):
    """
    Tests the creation of a paper using a controller
    :param db: initiated and loaded database
    """

    controller = PaperController(db=db)

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


def test_paper_delete(db: BaseDatabase):
    """
    Tests the deletion of a paper using a controller
    :param db: initiated and loaded database
    """

    controller = PaperController(db=db)

    paper_id = "paper-deletion"
    paper = Paper(
        arxiv_id=paper_id,
        arxiv_rev=1,
        title="Test Paper",
        submission_date=datetime.today().date(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    creation_id = controller.create(paper)
    deletion_id = controller.delete(paper_id)

    assert creation_id == deletion_id

    with pytest.raises(ValueError):
        controller.get(paper_id, 1)


def test_paper_delete_rev(db: BaseDatabase):
    """
    Tests the deletion of a paper using a controller
    :param db: initiated and loaded database
    """

    controller = PaperController(db=db)

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

    with pytest.raises(ValueError):
        controller.get(paper_id, paper_rev)


def test_paper_author_get(db: BaseDatabase):
    """
    Tests the retrieval of a paper author using a controller
    :param db: initiated and loaded database
    """

    controller = PaperAuthorController(db=db)
    all_authors = controller.get_by_paper("paper-01234", 1)
    one_author = all_authors[0]

    assert type(all_authors) == list
    assert type(one_author) is PaperAuthor
    assert one_author.id == "paper-author-01234-A"


def test_paper_ref_counter_get(db: BaseDatabase):
    """
    Tests the retrieval of a paper ref. counter using a controller
    :param db: initiated and loaded database
    """

    controller = PaperReferenceCountersController(db=db)
    all_counters = controller.get_by_paper("paper-01234", 1)
    one_counter = all_counters[0]

    assert type(all_counters) == list
    assert type(one_counter) is PaperReferenceCounters
    assert one_counter.id == "paper-ref-counter-01234-A"
