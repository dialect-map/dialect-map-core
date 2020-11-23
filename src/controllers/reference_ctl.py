# -*- coding: utf-8 -*-

from models import Paper
from models import PaperReference
from .base import StaticController


class ReferenceController(StaticController[PaperReference]):
    """
    Controller for the PaperReference objects (static)
    Extend as desired
    """

    data_model = PaperReference

    def get_by_source_paper(self, arxiv_id: str, arxiv_rev: int) -> list:
        """
        Gets a database record by its ID
        :param arxiv_id: ID of the reference source paper
        :param arxiv_rev: revision of the reference source paper
        :return: list of data object representing database records
        """

        query = self.db.session.query(self.data_model)
        query = query.filter(self.data_model.source_arxiv_id == arxiv_id)
        query = query.filter(self.data_model.source_arxiv_rev == arxiv_rev)

        return query.all()

    def get_by_target_paper(self, arxiv_id: str, arxiv_rev: int) -> list:
        """
        Gets a database record by its ID
        :param arxiv_id: ID of the reference target paper
        :param arxiv_rev: revision of the reference target paper
        :return: list of data object representing database records
        """

        query = self.db.session.query(self.data_model)
        query = query.filter(self.data_model.target_arxiv_id == arxiv_id)
        query = query.filter(self.data_model.target_arxiv_rev == arxiv_rev)

        return query.all()
