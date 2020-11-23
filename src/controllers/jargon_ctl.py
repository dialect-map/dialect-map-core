# -*- coding: utf-8 -*-

from models import Jargon
from models import JargonCategoryMetrics as JCategoryMetrics
from models import JargonPaperMetrics as JPaperMetrics
from models import Paper
from .base import StaticController


class JargonController(StaticController[Jargon]):
    """
    Controller for the jargon objects (static)
    Extend as desired
    """

    data_model = Jargon


class JargonCategoryMetricsController(StaticController[JCategoryMetrics]):
    """
    Controller for the jargon category metric objects
    Extend as desired
    """

    data_model = JCategoryMetrics

    def get_by_jargon(self, jargon_id: str, category_id: str = None) -> list:
        """
        Gets a database record by its ID
        :param jargon_id: ID of the metrics associated jargon
        :param category_id: ID of the metrics associated category (optional)
        :return: data object representing the database record
        """

        query = self.db.session.query(self.data_model)
        query = query.filter(self.data_model.jargon_id == jargon_id)

        if category_id:
            query = query.filter(self.data_model.category_id == category_id)

        return query.all()


class JargonPaperMetricsController(StaticController[JPaperMetrics]):
    """
    Controller for the jargon paper metric objects
    Extend as desired
    """

    data_model = JPaperMetrics

    def get_by_jargon(self, jargon_id: str, arxiv_id: str = None, arxiv_rev: int = None) -> list:
        """
        Gets a database record by its ID
        :param jargon_id: ID of the metrics associated jargon
        :param arxiv_id: ID of the metrics associated paper (optional)
        :param arxiv_rev: revision of the metrics associated paper (optional)
        :return: data object representing the database record
        """

        query = self.db.session.query(self.data_model)
        query = query.filter(self.data_model.jargon_id == jargon_id)

        if arxiv_id:
            query = query.filter(self.data_model.arxiv_id == arxiv_id)
        if arxiv_rev:
            query = query.filter(self.data_model.arxiv_rev == arxiv_rev)

        return query.all()
