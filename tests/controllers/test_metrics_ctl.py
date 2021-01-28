# -*- coding: utf-8 -*-

import pytest

from src.dialect_map.controllers import JargonCategoryMetricsController
from src.dialect_map.controllers import JargonPaperMetricsController
from src.dialect_map.models import JargonCategoryMetrics
from src.dialect_map.models import JargonPaperMetrics
from src.dialect_map.storage import BaseDatabase


@pytest.mark.usefixtures("database_rollback")
class TestCategoryMetricsController:
    """ Class to group all the CategoryMetric model controller tests """

    @pytest.fixture(scope="class")
    def controller(self, database: BaseDatabase):
        """
        Creates a memory-based controller for the CategoryMetric records
        :param database: dummy database instance
        :return: initiated controller instance
        """

        return JargonCategoryMetricsController(db=database)

    def test_get_by_jargon(self, controller: JargonCategoryMetricsController):
        """
        Tests the retrieval of a jargon category metrics by the controller
        :param controller: initiated instance
        """

        all_metrics = controller.get_by_jargon("jargon-01234", "category-01234")
        one_metric = all_metrics[0]

        assert type(all_metrics) == list
        assert type(one_metric) is JargonCategoryMetrics
        assert one_metric.id == "jargon-cat-metric-01234"


@pytest.mark.usefixtures("database_rollback")
class TestPaperMetricsController:
    """ Class to group all the PaperMetric model controller tests """

    @pytest.fixture(scope="class")
    def controller(self, database: BaseDatabase):
        """
        Creates a memory-based controller for the PaperMetric records
        :param database: dummy database instance
        :return: initiated controller instance
        """

        return JargonPaperMetricsController(db=database)

    def test_get_by_jargon(self, controller: JargonPaperMetricsController):
        """
        Tests the retrieval of a jargon paper metrics by the controller
        :param controller: initiated instance
        """

        all_metrics = controller.get_by_jargon("jargon-01234", "paper-01234", 1)
        one_metric = all_metrics[0]

        assert type(all_metrics) == list
        assert type(one_metric) is JargonPaperMetrics
        assert one_metric.id == "jargon-paper-metric-00001"

    def test_get_latest(self, controller: JargonPaperMetricsController):
        """
        Tests the retrieval of the latest jargon paper metrics by the controller
        :param controller: initiated instance
        """

        all_metrics = controller.get_latest_by_jargon("jargon-01234")

        assert type(all_metrics) == list
        assert all(m.arxiv_rev > 1 for m in all_metrics)
