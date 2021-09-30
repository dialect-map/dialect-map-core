# -*- coding: utf-8 -*-

from sqlalchemy.orm import Query
from sqlalchemy.sql import and_
from sqlalchemy.sql import func
from sqlalchemy.sql import distinct

from .base import StaticController
from ..models import JargonCategoryMetrics as JCategoryMetrics
from ..models import JargonPaperMetrics as JPaperMetrics


class JargonCategoryMetricsController(StaticController[JCategoryMetrics]):
    """
    Controller for the jargon category metric objects
    Extend as desired
    """

    model = JCategoryMetrics

    def get_by_jargon(self, jargon_id: str, category_id: str = None) -> list:
        """
        Gets a list of category jargon metrics
        :param jargon_id: ID of the metrics associated jargon
        :param category_id: ID of the metrics associated category (optional)
        :return: list of database objects
        """

        query = self.db.session.query(self.model)
        query = query.filter(self.model.jargon_id == jargon_id)

        if category_id:
            query = query.filter(self.model.category_id == category_id)

        return query.all()


class JargonPaperMetricsController(StaticController[JPaperMetrics]):
    """
    Controller for the jargon paper metric objects
    Extend as desired
    """

    model = JPaperMetrics

    def _build_latest_rev_subquery(self) -> Query:
        """
        Builds an SQL subquery to select the latest revision of each ID
        :return: SQL subquery
        """

        return (
            self.db.session.query(
                distinct(self.model.arxiv_id).label("arxiv_id"),
                func.max(self.model.arxiv_rev).label("latest_rev"),
            )
            .group_by(self.model.arxiv_id)
            .subquery()
        )

    def get_by_jargon(self, jargon_id: str, arxiv_id: str = None, arxiv_rev: int = None) -> list:
        """
        Gets a list of paper jargon metrics
        :param jargon_id: ID of the metrics associated jargon
        :param arxiv_id: ID of the metrics associated paper (optional)
        :param arxiv_rev: revision of the metrics associated paper (optional)
        :return: list of database objects
        """

        query = self.db.session.query(self.model)
        query = query.filter(self.model.jargon_id == jargon_id)

        if arxiv_id:
            query = query.filter(self.model.arxiv_id == arxiv_id)
        if arxiv_rev:
            query = query.filter(self.model.arxiv_rev == arxiv_rev)

        return query.all()

    def get_latest_by_jargon(self, jargon_id: str) -> list:
        """
        Gets the latest paper jargon metrics given a jargon ID
        :param jargon_id: ID of the metrics associated jargon
        :return: list of database objects
        """

        subquery = self._build_latest_rev_subquery()

        query = self.db.session.query(self.model)
        query = query.filter(self.model.jargon_id == jargon_id)
        query = query.join(
            subquery,
            and_(
                self.model.arxiv_id == subquery.c.arxiv_id,
                self.model.arxiv_rev == subquery.c.latest_rev,
            ),
        )

        return query.all()
