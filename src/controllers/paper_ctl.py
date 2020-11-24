# -*- coding: utf-8 -*-

from models import Paper
from models import PaperAuthor
from models import PaperReferenceCounters
from .base import StaticController
from .base import EvolvingController


class PaperController(EvolvingController[Paper]):
    """
    Controller for the Paper objects (evolving)
    Extend as desired
    """

    data_model = Paper


class PaperAuthorController(StaticController[PaperAuthor]):
    """
    Controller for the PaperAuthor objects (static)
    Extend as desired
    """

    data_model = PaperAuthor

    def get_by_paper(self, arxiv_id: str, arxiv_rev: int) -> list:
        """
        Gets a database record by its ID
        :param arxiv_id: ID of the metrics associated paper
        :param arxiv_rev: revision of the metrics associated paper
        :return: list of data object representing database records
        """

        query = self.db.session.query(self.data_model)
        query = query.filter(self.data_model.arxiv_id == arxiv_id)
        query = query.filter(self.data_model.arxiv_rev == arxiv_rev)

        return query.all()


class PaperReferenceCountersController(StaticController[PaperReferenceCounters]):
    """
    Controller for the PaperReferenceCounter objects (static)
    Extend as desired
    """

    data_model = PaperReferenceCounters

    def get_by_paper(self, arxiv_id: str, arxiv_rev: int) -> list:
        """
        Gets a database record by its ID
        :param arxiv_id: ID of the metrics associated paper
        :param arxiv_rev: revision of the metrics associated paper
        :return: list of data object representing database records
        """

        query = self.db.session.query(self.data_model)
        query = query.filter(self.data_model.arxiv_id == arxiv_id)
        query = query.filter(self.data_model.arxiv_rev == arxiv_rev)

        return query.all()
