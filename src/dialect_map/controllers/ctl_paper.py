# -*- coding: utf-8 -*-

from .base import StaticController
from .base import EvolvingController
from ..models import Paper
from ..models import PaperAuthor
from ..models import PaperReferenceCounters


class PaperController(EvolvingController):
    """
    Controller for the Paper objects (evolving)
    Extend as desired
    """

    model = Paper


class PaperAuthorController(StaticController):
    """
    Controller for the PaperAuthor objects (static)
    Extend as desired
    """

    model = PaperAuthor

    def get_by_paper(self, arxiv_id: str, arxiv_rev: int) -> list:
        """
        Gets a list paper authors given a paper
        :param arxiv_id: ID of the metrics associated paper
        :param arxiv_rev: revision of the metrics associated paper
        :return: list of database objects
        """

        query = self.session.query(self.model)
        query = query.filter(self.model.arxiv_id == arxiv_id)
        query = query.filter(self.model.arxiv_rev == arxiv_rev)

        return query.all()


class PaperReferenceCountersController(StaticController):
    """
    Controller for the PaperReferenceCounter objects (static)
    Extend as desired
    """

    model = PaperReferenceCounters

    def get_by_paper(self, arxiv_id: str, arxiv_rev: int) -> list:
        """
        Gets a list of paper reference counters given a paper
        :param arxiv_id: ID of the metrics associated paper
        :param arxiv_rev: revision of the metrics associated paper
        :return: list of database objects
        """

        query = self.session.query(self.model)
        query = query.filter(self.model.arxiv_id == arxiv_id)
        query = query.filter(self.model.arxiv_rev == arxiv_rev)

        return query.all()
