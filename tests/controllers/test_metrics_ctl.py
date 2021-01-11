# -*- coding: utf-8 -*-

from src.dialect_map.controllers import JargonCategoryMetricsController
from src.dialect_map.controllers import JargonPaperMetricsController
from src.dialect_map.models import JargonCategoryMetrics
from src.dialect_map.models import JargonPaperMetrics
from src.dialect_map.storage import BaseDatabase


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
    assert one_metric.id == "jargon-paper-metric-00001"


def test_jargon_paper_metrics_get_latest(db: BaseDatabase):
    """
    Tests the retrieval of the latest jargon paper metrics using a controller
    :param db: initiated and loaded database
    """

    controller = JargonPaperMetricsController(db=db)
    all_metrics = controller.get_latest_by_jargon("jargon-01234")

    assert type(all_metrics) == list

    for metric in all_metrics:
        assert metric.arxiv_rev > 1
