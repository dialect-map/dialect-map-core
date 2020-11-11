# -*- coding: utf-8 -*-

from models import Paper
from models import PaperReference
from storage import BaseDatabase
from .base import BaseController


class ReferenceController(BaseController):
    """ Controller for the PaperReference objects """

    def __init__(self, db: BaseDatabase):
        """
        Initializes the controller with the underlying database
        :param db: database engine to use
        """

        self.db = db

    def get(self, id: str) -> PaperReference:
        """
        Gets a database record by its ID
        :param id: ID of the database entry
        :return: data object representing the database record
        """

        query = self.db.session.query(PaperReference)
        reference = query.get(id)

        if reference is None:
            raise ValueError(f"Unknown reference: {id}")

        return reference

    def get_by_source_paper(self, arxiv_id: str, arxiv_rev: str = None) -> list:
        """
        Gets a database record by its ID
        :param arxiv_id: ID of the reference source paper
        :param arxiv_rev: revision of the reference source paper (optional)
        :return: list of data object representing database records
        """

        if not arxiv_rev:
            arxiv_rev = Paper.default_revision

        query = self.db.session.query(PaperReference)
        query = query.filter(PaperReference.source_arxiv_id == arxiv_id)
        query = query.filter(PaperReference.source_arxiv_rev == arxiv_rev)

        return query.all()

    def get_by_target_paper(self, arxiv_id: str, arxiv_rev: str = None) -> list:
        """
        Gets a database record by its ID
        :param arxiv_id: ID of the reference target paper
        :param arxiv_rev: revision of the reference target paper (optional)
        :return: list of data object representing database records
        """

        if not arxiv_rev:
            arxiv_rev = Paper.default_revision

        query = self.db.session.query(PaperReference)
        query = query.filter(PaperReference.target_arxiv_id == arxiv_id)
        query = query.filter(PaperReference.target_arxiv_rev == arxiv_rev)

        return query.all()

    def create(self, reference: PaperReference) -> str:
        """
        Creates a new database record given its object properties
        :param reference: paper reference object to create the record with
        :return: ID of the created paper reference
        """

        try:
            self.db.session.add(reference)
            self.db.session.commit()
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        return reference.id

    def delete(self, id: str) -> str:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :return: ID of the deleted paper reference
        """

        self.db.session.delete(self.get(id))
        self.db.session.commit()
        return id
