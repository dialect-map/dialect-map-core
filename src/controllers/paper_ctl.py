# -*- coding: utf-8 -*-

from models import Paper
from models import PaperAuthor
from models import PaperReferenceCounters
from storage import BaseDatabase
from .base import BaseController


class PaperController(BaseController):
    """ Controller for the Paper objects """

    def __init__(self, db: BaseDatabase):
        """
        Initializes the controller with the underlying database
        :param db: database engine to use
        """

        self.db = db

    def get(self, id: str, rev: str = None) -> Paper:
        """
        Gets a database record by its ID
        :param id: ID of the database entry
        :param rev: revision of the database entry (optional)
        :return: data object representing the database record
        """

        if not rev:
            rev = Paper.default_revision

        query = self.db.session.query(Paper)
        query = query.filter(Paper.arxiv_id == id)
        query = query.filter(Paper.arxiv_rev == rev)
        paper = query.one_or_none()

        if paper is None:
            raise ValueError(f"Unknown paper: {id} - Revision: {rev}")

        return paper

    def create(self, paper: Paper) -> str:
        """
        Creates a new database record given its object properties
        :param paper: paper object to create the record with
        :return: ID of the created paper
        """

        try:
            self.db.session.add(paper)
            self.db.session.commit()
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        return paper.arxiv_id

    def delete(self, id: str) -> str:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :return: ID of the deleted paper
        """

        self.db.session.delete(self.get(id))
        self.db.session.commit()
        return id


class PaperAuthorController(BaseController):
    """ Controller for the PaperAuthor objects """

    def __init__(self, db: BaseDatabase):
        """
        Initializes the controller with the underlying database
        :param db: database engine to use
        """

        self.db = db

    def get(self, id: str) -> PaperAuthor:
        """
        Gets a database record by its ID
        :param id: ID of the database entry
        :return: data object representing the database record
        """

        query = self.db.session.query(PaperAuthor)
        author = query.get(id)

        if author is None:
            raise ValueError(f"Unknown author: {id}")

        return author

    def get_by_paper(self, arxiv_id: str, arxiv_rev: str = None) -> list:
        """
        Gets a database record by its ID
        :param arxiv_id: ID of the metrics associated paper
        :param arxiv_rev: revision of the metrics associated paper (optional)
        :return: list of data object representing database records
        """

        if not arxiv_rev:
            arxiv_rev = Paper.default_revision

        query = self.db.session.query(PaperAuthor)
        query = query.filter(PaperAuthor.arxiv_id == arxiv_id)
        query = query.filter(PaperAuthor.arxiv_rev == arxiv_rev)

        return query.all()

    def create(self, author: PaperAuthor) -> str:
        """
        Creates a new database record given its object properties
        :param author: author object to create the record with
        :return: ID of the created paper author
        """

        try:
            self.db.session.add(author)
            self.db.session.commit()
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        return author.author_id

    def delete(self, id: str) -> str:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :return: ID of the deleted paper author
        """

        self.db.session.delete(self.get(id))
        self.db.session.commit()
        return id


class PaperReferenceCountersController(BaseController):
    """ Controller for the PaperReferenceCounter objects """

    def __init__(self, db: BaseDatabase):
        """
        Initializes the controller with the underlying database
        :param db: database engine to use
        """

        self.db = db

    def get(self, id: str) -> PaperReferenceCounters:
        """
        Gets a database record by its ID
        :param id: ID of the database entry
        :return: data object representing the database record
        """

        query = self.db.session.query(PaperAuthor)
        counters = query.get(id)

        if counters is None:
            raise ValueError(f"Unknown reference counters: {id}")

        return counters

    def get_by_paper(self, arxiv_id: str, arxiv_rev: str = None) -> list:
        """
        Gets a database record by its ID
        :param arxiv_id: ID of the metrics associated paper
        :param arxiv_rev: revision of the metrics associated paper (optional)
        :return: list of data object representing database records
        """

        if not arxiv_rev:
            arxiv_rev = Paper.default_revision

        query = self.db.session.query(PaperReferenceCounters)
        query = query.filter(PaperReferenceCounters.arxiv_id == arxiv_id)
        query = query.filter(PaperReferenceCounters.arxiv_rev == arxiv_rev)

        return query.all()

    def create(self, counters: PaperReferenceCounters) -> str:
        """
        Creates a new database record given its object properties
        :param counters: reference counters object to create the record with
        :return: ID of the created paper reference counters
        """

        try:
            self.db.session.add(counters)
            self.db.session.commit()
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        return counters.ref_id

    def delete(self, id: str) -> str:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :return: ID of the deleted paper reference counters
        """

        self.db.session.delete(self.get(id))
        self.db.session.commit()
        return id
