# -*- coding: utf-8 -*-

from .base import StaticController
from .base import EvolvingController
from ..models import Paper
from ..models import PaperAuthor
from ..models import PaperReferenceCounters


class PaperController(EvolvingController[Paper]):
    """
    Controller for the Paper objects (evolving)
    Extend as desired
    """

    model = Paper


class PaperAuthorController(StaticController[PaperAuthor]):
    """
    Controller for the PaperAuthor objects (static)
    Extend as desired
    """

    model = PaperAuthor

    def get_by_paper(self, arxiv_id: str, arxiv_rev: int) -> list:
        """
        Gets a database record by its ID
        :param arxiv_id: ID of the metrics associated paper
        :param arxiv_rev: revision of the metrics associated paper
        :return: list of data object representing database records
        """

        query = self.db.session.query(self.model)
        query = query.filter(self.model.arxiv_id == arxiv_id)
        query = query.filter(self.model.arxiv_rev == arxiv_rev)

        return query.all()


class PaperReferenceCountersController(StaticController[PaperReferenceCounters]):
    """
    Controller for the PaperReferenceCounter objects (static)
    Extend as desired
    """

    model = PaperReferenceCounters

    def get_by_paper(self, arxiv_id: str, arxiv_rev: int) -> list:
        """
        Gets a database record by its ID
        :param arxiv_id: ID of the metrics associated paper
        :param arxiv_rev: revision of the metrics associated paper
        :return: list of data object representing database records
        """

        query = self.db.session.query(self.model)
        query = query.filter(self.model.arxiv_id == arxiv_id)
        query = query.filter(self.model.arxiv_rev == arxiv_rev)

        return query.all()
