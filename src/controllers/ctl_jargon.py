# -*- coding: utf-8 -*-

from models import Jargon
from models import JargonCategoryMetrics as JCategoryMetrics
from models import JargonPaperMetrics as JPaperMetrics
from sqlalchemy import and_
from sqlalchemy import func
from .base import StaticController


class JargonController(StaticController[Jargon]):
    """
    Controller for the jargon objects (static)
    Extend as desired
    """

    model = Jargon

    def get_by_string(self, jargon_str: str) -> Jargon:
        """
        Gets a database record by its string value
        :param jargon_str: jargon string representation
        :return: data object representing the database record
        """

        query = self.db.session.query(self.model)
        query = query.filter(self.model.jargon_str == jargon_str)

        return query.one_or_none()


class JargonCategoryMetricsController(StaticController[JCategoryMetrics]):
    """
    Controller for the jargon category metric objects
    Extend as desired
    """

    model = JCategoryMetrics

    def get_by_jargon(self, jargon_id: str, category_id: str = None) -> list:
        """
        Gets a database record by its ID
        :param jargon_id: ID of the metrics associated jargon
        :param category_id: ID of the metrics associated category (optional)
        :return: data objects representing the database records
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

    def get_by_jargon(self, jargon_id: str, arxiv_id: str = None, arxiv_rev: int = None) -> list:
        """
        Gets a database record by its ID
        :param jargon_id: ID of the metrics associated jargon
        :param arxiv_id: ID of the metrics associated paper (optional)
        :param arxiv_rev: revision of the metrics associated paper (optional)
        :return: data objects representing the database records
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
        Gets latest paper metric records by jargon ID
        :param jargon_id: ID of the metrics associated jargon
        :return: data objects representing the database records
        """

        subquery = (
            self.db.session.query(
                self.model.arxiv_id, func.max(self.model.arxiv_rev).label("latest_rev")
            )
            .group_by(self.model.arxiv_id)
            .subquery()
        )

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
