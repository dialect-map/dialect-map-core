# -*- coding: utf-8 -*-

from datetime import datetime

import pytest

from src.dialect_map.controllers import JargonCategoryMetricsController
from src.dialect_map.controllers import JargonPaperMetricsController
from src.dialect_map.models import JargonCategoryMetrics
from src.dialect_map.models import JargonPaperMetrics
from src.dialect_map.storage import BaseDatabase


@pytest.mark.usefixtures("rollback")
@pytest.mark.usefixtures("session")
class TestCategoryMetricsController:
    """Class to group all the CategoryMetric model controller tests"""

    @pytest.fixture(scope="class")
    def controller(self, session: object):
        """
        Creates a memory-based controller for the CategoryMetric records
        :param session: database session instance
        :return: initiated controller instance
        """

        return JargonCategoryMetricsController(session)

    def test_get_by_jargon(self, controller: JargonCategoryMetricsController):
        """
        Tests the retrieval of a jargon category metric by the controller
        :param controller: initiated instance
        """

        all_metrics = controller.get_by_jargon("jargon-01234", "category-01234")
        one_metric = all_metrics[0]

        assert type(all_metrics) == list
        assert type(one_metric) is JargonCategoryMetrics
        assert one_metric.id == "jargon-cat-metric-01234"

    def test_create_with_non_existent_jargon(
        self,
        database: BaseDatabase,
        controller: JargonCategoryMetricsController,
    ):
        """
        Tests the creation of a jargon category metric by the controller
        when the referenced jargon does not exist
        :param database: dummy database instance
        :param controller: initiated instance
        """

        cat_metrics = JargonCategoryMetrics(
            jargon_id="non-existing-jargon",
            category_id="category-01234",
            abs_freq=10,
            rel_freq=0.05,
            created_at=datetime.utcnow(),
        )

        assert pytest.raises(database.error, controller.create, cat_metrics)

    def test_create_with_non_existent_category(
        self,
        database: BaseDatabase,
        controller: JargonCategoryMetricsController,
    ):
        """
        Tests the creation of a jargon category metric by the controller
        when the referenced category does not exist
        :param database: dummy database instance
        :param controller: initiated instance
        """

        cat_metrics = JargonCategoryMetrics(
            jargon_id="jargon-01234",
            category_id="non-existing-category",
            abs_freq=10,
            rel_freq=0.05,
            created_at=datetime.utcnow(),
        )

        assert pytest.raises(database.error, controller.create, cat_metrics)


@pytest.mark.usefixtures("rollback")
@pytest.mark.usefixtures("session")
class TestPaperMetricsController:
    """Class to group all the PaperMetric model controller tests"""

    @pytest.fixture(scope="class")
    def controller(self, session: object):
        """
        Creates a memory-based controller for the PaperMetric records
        :param session: database session instance
        :return: initiated controller instance
        """

        return JargonPaperMetricsController(session)

    def test_get_by_jargon(self, controller: JargonPaperMetricsController):
        """
        Tests the retrieval of a jargon paper metric by the controller
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
        assert len(all_metrics) > 0
        assert all(m.arxiv_rev > 1 for m in all_metrics)

    def test_create_with_non_existent_jargon(
        self,
        database: BaseDatabase,
        controller: JargonPaperMetricsController,
    ):
        """
        Tests the creation of a jargon paper metric by the controller
        when the referenced jargon does not exist
        :param database: dummy database instance
        :param controller: initiated instance
        """

        paper_metrics = JargonPaperMetrics(
            jargon_id="non-existing-jargon",
            arxiv_id="paper-01234",
            arxiv_rev=1,
            abs_freq=10,
            rel_freq=0.05,
            created_at=datetime.utcnow(),
        )

        assert pytest.raises(database.error, controller.create, paper_metrics)

    def test_create_with_non_existent_category(
        self,
        database: BaseDatabase,
        controller: JargonPaperMetricsController,
    ):
        """
        Tests the creation of a jargon paper metric by the controller
        when the referenced category does not exist
        :param database: dummy database instance
        :param controller: initiated instance
        """

        paper_metrics = JargonPaperMetrics(
            jargon_id="jargon-01234",
            arxiv_id="non-existing-paper",
            arxiv_rev=1,
            abs_freq=10,
            rel_freq=0.05,
            created_at=datetime.utcnow(),
        )

        assert pytest.raises(database.error, controller.create, paper_metrics)
