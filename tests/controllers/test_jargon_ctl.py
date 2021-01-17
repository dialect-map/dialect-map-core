# -*- coding: utf-8 -*-

import pytest
from datetime import datetime
from src.dialect_map.controllers import JargonController
from src.dialect_map.controllers import JargonGroupController
from src.dialect_map.models import Jargon
from src.dialect_map.models import JargonGroup
from src.dialect_map.storage import BaseDatabase


def test_jargon_get(db: BaseDatabase):
    """
    Tests the retrieval of a jargon using a controller
    :param db: initiated and loaded database
    """

    controller = JargonController(db=db)
    jargon = controller.get("jargon-01234")

    assert type(jargon) is Jargon
    assert jargon.id == "jargon-01234"


def test_jargon_get_by_string(db: BaseDatabase):
    """
    Tests the retrieval of a jargon using a controller
    :param db: initiated and loaded database
    """

    controller = JargonController(db=db)
    jargon = controller.get_by_string("One string")

    assert type(jargon) is Jargon
    assert jargon.id == "jargon-01234"


def test_jargon_get_by_group(db: BaseDatabase):
    """
    Tests the retrieval of jargon groups using a controller
    :param db: initiated and loaded database
    """

    controller = JargonController(db=db)
    groups = controller.get_by_group()

    assert type(groups) is list
    assert len(groups) == 1
    assert len(groups[0]) == 2


def test_jargon_create(db: BaseDatabase):
    """
    Tests the creation of a jargon using a controller
    :param db: initiated and loaded database
    """

    controller = JargonController(db=db)

    jargon_id = "jargon-creation"
    jargon_ds = "My test jargon"
    jargon_re = "[Mm]y test jargon"
    jargon = Jargon(
        jargon_id=jargon_id,
        jargon_str=jargon_ds,
        jargon_regex=jargon_re,
        num_words=len(jargon_ds.split(" ")),
        created_at=datetime.now(),
    )

    creation_id = controller.create(jargon)
    created_obj = controller.get(jargon_id)

    assert creation_id == jargon_id
    assert created_obj == jargon


def test_jargon_delete(db: BaseDatabase):
    """
    Tests the deletion of a jargon using a controller
    :param db: initiated and loaded database
    """

    controller = JargonController(db=db)

    jargon_id = "jargon-deletion"
    jargon_ds = "My test jargon"
    jargon_re = "[Mm]y test jargon"
    jargon = Jargon(
        jargon_id=jargon_id,
        jargon_str=jargon_ds,
        jargon_regex=jargon_re,
        num_words=len(jargon_ds.split(" ")),
        created_at=datetime.now(),
    )

    creation_id = controller.create(jargon)
    deletion_id = controller.delete(jargon_id)

    assert creation_id == deletion_id

    with pytest.raises(ValueError):
        controller.get(jargon_id)


def test_jargon_group_get(db: BaseDatabase):
    """
    Tests the retrieval of a jargon group using a controller
    :param db: initiated and loaded database
    """

    controller = JargonGroupController(db=db)
    group = controller.get("jargon-group-01234")

    assert type(group) is JargonGroup
    assert group.id == "jargon-group-01234"


def test_jargon_group_create(db: BaseDatabase):
    """
    Tests the creation of a jargon group using a controller
    :param db: initiated and loaded database
    """

    controller = JargonGroupController(db=db)

    group_id = "jargon-group-creation"
    group_ds = "My test group"
    group = JargonGroup(
        group_id=group_id,
        description=group_ds,
        created_at=datetime.now(),
    )

    creation_id = controller.create(group)
    created_obj = controller.get(group_id)

    assert creation_id == group_id
    assert created_obj == group


def test_jargon_group_delete(db: BaseDatabase):
    """
    Tests the deletion of a jargon group using a controller
    :param db: initiated and loaded database
    """

    controller = JargonGroupController(db=db)

    group_id = "jargon-group-deletion"
    group_ds = "My test group"
    group = JargonGroup(
        group_id=group_id,
        description=group_ds,
        created_at=datetime.now(),
    )

    creation_id = controller.create(group)
    deletion_id = controller.delete(group_id)

    assert creation_id == deletion_id

    with pytest.raises(ValueError):
        controller.get(group_id)
