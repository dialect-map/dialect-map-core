# -*- coding: utf-8 -*-

from .base import StaticController
from ..models import PaperReference


class ReferenceController(StaticController):
    """
    Controller for the PaperReference objects (static)
    Extend as desired
    """

    model = PaperReference

    def get_by_source_paper(self, arxiv_id: str, arxiv_rev: int) -> list:
        """
        Gets a list of paper references given the source
        :param arxiv_id: ID of the reference source paper
        :param arxiv_rev: revision of the reference source paper
        :return: list of database objects
        """

        query = self.db.session.query(self.model)
        query = query.filter(self.model.source_arxiv_id == arxiv_id)
        query = query.filter(self.model.source_arxiv_rev == arxiv_rev)

        return query.all()

    def get_by_target_paper(self, arxiv_id: str, arxiv_rev: int) -> list:
        """
        Gets a list of paper references given the target
        :param arxiv_id: ID of the reference target paper
        :param arxiv_rev: revision of the reference target paper
        :return: list of database objects
        """

        query = self.db.session.query(self.model)
        query = query.filter(self.model.target_arxiv_id == arxiv_id)
        query = query.filter(self.model.target_arxiv_rev == arxiv_rev)

        return query.all()
