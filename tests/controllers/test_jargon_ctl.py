# -*- coding: utf-8 -*-

import pytest
from controllers import JargonController
from controllers import JargonCategoryMetricsController
from controllers import JargonPaperMetricsController
from datetime import datetime
from models import Jargon
from models import JargonCategoryMetrics
from models import JargonPaperMetrics
from storage import BaseDatabase


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


def test_jargon_create(db: BaseDatabase):
    """
    Tests the creation of a jargon using a controller
    :param db: initiated and loaded database
    """

    controller = JargonController(db=db)

    jargon_id = "jargon-creation"
    jargon_ds = "My test jargon"
    jargon = Jargon(
        jargon_id=jargon_id,
        jargon_str=jargon_ds,
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
    jargon = Jargon(
        jargon_id=jargon_id,
        jargon_str=jargon_ds,
        num_words=len(jargon_ds.split(" ")),
        created_at=datetime.now(),
    )

    creation_id = controller.create(jargon)
    deletion_id = controller.delete(jargon_id)

    assert creation_id == deletion_id

    with pytest.raises(ValueError):
        controller.get(jargon_id)


def test_jargon_cat_metrics_get(db: BaseDatabase):
    """
    Tests the retrieval of a jargon category metrics using a controller
    :param db: initiated and loaded database
    """

    controller = JargonCategoryMetricsController(db=db)
    all_metrics = controller.get_by_jargon("jargon-01234", "category-01234")
    one_metric = all_metrics[0]

    assert type(all_metrics) == list
    assert type(one_metric) is JargonCategoryMetrics
    assert one_metric.id == "jargon-cat-metric-01234"


def test_jargon_paper_metrics_get(db: BaseDatabase):
    """
    Tests the retrieval of a jargon paper metrics using a controller
    :param db: initiated and loaded database
    """

    controller = JargonPaperMetricsController(db=db)
    all_metrics = controller.get_by_jargon("jargon-01234", "paper-01234", 1)
    one_metric = all_metrics[0]

    assert type(all_metrics) == list
    assert type(one_metric) is JargonPaperMetrics
    assert one_metric.id == "jargon-paper-metric-01234"
