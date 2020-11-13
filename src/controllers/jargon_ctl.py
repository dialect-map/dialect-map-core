# -*- coding: utf-8 -*-

from models import Jargon
from models import JargonCategoryMetrics as JCategoryMetrics
from models import JargonPaperMetrics as JPaperMetrics
from models import Paper
from storage import BaseDatabase
from .base import BaseController


class JargonController(BaseController):
    """ Controller for the jargon objects """

    def __init__(self, db: BaseDatabase):
        """
        Initializes the controller with the underlying database
        :param db: database engine to use
        """

        self.db = db

    def get(self, id: str) -> Jargon:
        """
        Gets a database record by its ID
        :param id: ID of the database entry
        :return: data object representing the database record
        """

        query = self.db.session.query(Jargon)
        jargon = query.get(id)

        if jargon is None:
            raise ValueError(f"Unknown jargon: {id}")

        return jargon

    def create(self, jargon: Jargon) -> str:
        """
        Creates a new database record given its object properties
        :param jargon: jargon object to create the record with
        :return: ID of the created jargon
        """

        try:
            self.db.session.add(jargon)
            self.db.session.commit()
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        return jargon.jargon_id

    def delete(self, id: str) -> str:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :return: ID of the deleted jargon
        """

        self.db.session.delete(self.get(id))
        self.db.session.commit()
        return id


class JargonCategoryMetricsController(BaseController):
    """ Controller for the jargon category metric objects """

    def __init__(self, db: BaseDatabase):
        """
        Initializes the controller with the underlying database
        :param db: database engine to use
        """

        self.db = db

    def get(self, id: str) -> JCategoryMetrics:
        """
        Gets a database record by its ID
        :param id: ID of the database entry
        :return: data object representing the database record
        """

        query = self.db.session.query(JCategoryMetrics)
        metrics = query.get(id)

        if metrics is None:
            raise ValueError(f"Unknown metrics: {id}")

        return metrics

    def get_by_jargon(self, jargon_id: str, category_id: str = None) -> list:
        """
        Gets a database record by its ID
        :param jargon_id: ID of the metrics associated jargon
        :param category_id: ID of the metrics associated category (optional)
        :return: data object representing the database record
        """

        query = self.db.session.query(JCategoryMetrics)
        query = query.filter(JCategoryMetrics.jargon_id == jargon_id)

        if category_id:
            query = query.filter(JCategoryMetrics.category_id == category_id)

        return query.all()

    def create(self, metrics: JCategoryMetrics) -> str:
        """
        Creates a new database record given its object properties
        :param metrics: metrics object to create the record with
        :return: ID of the created metrics
        """

        try:
            self.db.session.add(metrics)
            self.db.session.commit()
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        return metrics.metric_id

    def delete(self, id: str) -> str:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :return: ID of the deleted metrics
        """

        self.db.session.delete(self.get(id))
        self.db.session.commit()
        return id


class JargonPaperMetricsController(BaseController):
    """ Controller for the jargon paper metric objects """

    def __init__(self, db: BaseDatabase):
        """
        Initializes the controller with the underlying database
        :param db: database engine to use
        """

        self.db = db

    def get(self, id: str) -> JPaperMetrics:
        """
        Gets a database record by its ID
        :param id: ID of the database entry
        :return: data object representing the database record
        """

        query = self.db.session.query(JPaperMetrics)
        metrics = query.get(id)

        if metrics is None:
            raise ValueError(f"Unknown metrics: {id}")

        return metrics

    def get_by_jargon(self, jargon_id: str, arxiv_id: str = None, arxiv_rev: str = None) -> list:
        """
        Gets a database record by its ID
        :param jargon_id: ID of the metrics associated jargon
        :param arxiv_id: ID of the metrics associated paper (optional)
        :param arxiv_rev: revision of the metrics associated paper (optional)
        :return: data object representing the database record
        """

        if arxiv_id and not arxiv_rev:
            arxiv_rev = Paper.default_revision

        query = self.db.session.query(JPaperMetrics)
        query = query.filter(JPaperMetrics.jargon_id == jargon_id)
        query = query.filter(JPaperMetrics.arxiv_id == arxiv_id)
        query = query.filter(JPaperMetrics.arxiv_rev == arxiv_rev)

        return query.all()

    def create(self, metrics: JPaperMetrics) -> str:
        """
        Creates a new database record given its object properties
        :param metrics: metrics object to create the record with
        :return: ID of the created metrics
        """

        try:
            self.db.session.add(metrics)
            self.db.session.commit()
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        return metrics.metric_id

    def delete(self, id: str) -> str:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :return: ID of the deleted metrics
        """

        self.db.session.delete(self.get(id))
        self.db.session.commit()
        return id
