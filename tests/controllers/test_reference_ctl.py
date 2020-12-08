# -*- coding: utf-8 -*-

import pytest
from datetime import datetime
from src.dialect_map.controllers import ReferenceController
from src.dialect_map.models import PaperReference
from src.dialect_map.storage import BaseDatabase


def test_reference_get(db: BaseDatabase):
    """
    Tests the retrieval of a paper reference using a controller
    :param db: initiated and loaded database
    """

    controller = ReferenceController(db=db)
    reference = controller.get("reference-01234")

    assert type(reference) is PaperReference
    assert reference.id == "reference-01234"


def test_reference_get_by_source(db: BaseDatabase):
    """
    Tests the retrieval of a paper reference with the source paper
    :param db: initiated and loaded database
    """

    controller = ReferenceController(db=db)

    source_paper_id = "paper-01234"
    source_paper_rev = 1

    all_refs = controller.get_by_source_paper(
        arxiv_id=source_paper_id,
        arxiv_rev=source_paper_rev,
    )
    one_ref = all_refs[0]

    assert type(all_refs) == list
    assert type(one_ref) is PaperReference
    assert one_ref.source_arxiv_id == source_paper_id
    assert one_ref.source_arxiv_rev == source_paper_rev


def test_reference_get_by_target(db: BaseDatabase):
    """
    Tests the retrieval of a paper reference with the target paper
    :param db: initiated and loaded database
    """

    controller = ReferenceController(db=db)

    target_paper_id = "paper-56789"
    target_paper_rev = 1

    all_refs = controller.get_by_target_paper(
        arxiv_id=target_paper_id,
        arxiv_rev=target_paper_rev,
    )
    one_ref = all_refs[0]

    assert type(all_refs) == list
    assert type(one_ref) is PaperReference
    assert one_ref.target_arxiv_id == target_paper_id
    assert one_ref.target_arxiv_rev == target_paper_rev


def test_reference_create(db: BaseDatabase):
    """
    Tests the creation of a reference using a controller
    :param db: initiated and loaded database
    """

    controller = ReferenceController(db=db)

    ref_id = "reference-creation"
    ref = PaperReference(
        reference_id=ref_id,
        source_arxiv_id="paper-01234",
        source_arxiv_rev=1,
        target_arxiv_id="paper-56789",
        target_arxiv_rev=1,
        created_at=datetime.now(),
    )

    creation_id = controller.create(ref)
    created_obj = controller.get(ref_id)

    assert creation_id == ref_id
    assert created_obj == ref


def test_reference_delete(db: BaseDatabase):
    """
    Tests the deletion of a reference using a controller
    :param db: initiated and loaded database
    """

    controller = ReferenceController(db=db)

    ref_id = "reference-deletion"
    ref = PaperReference(
        reference_id=ref_id,
        source_arxiv_id="paper-01234",
        source_arxiv_rev=1,
        target_arxiv_id="paper-56789",
        target_arxiv_rev=1,
        created_at=datetime.now(),
    )

    creation_id = controller.create(ref)
    deletion_id = controller.delete(ref_id)

    assert creation_id == deletion_id

    with pytest.raises(ValueError):
        controller.get(ref_id)
