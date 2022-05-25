# -*- coding: utf-8 -*-

from .base import StaticController
from ..models import CategoryMembership


class MembershipController(StaticController):
    """
    Controller for the membership objects (static)
    Extend as desired
    """

    model = CategoryMembership

    def get_by_paper(self, arxiv_id: str, arxiv_rev: int) -> list:
        """
        Gets a list of category memberships given a paper
        :param arxiv_id: ID of the reference source paper
        :param arxiv_rev: revision of the reference source paper
        :return: list of database objects
        """

        query = self.db.session.query(self.model)
        query = query.filter(self.model.arxiv_id == arxiv_id)
        query = query.filter(self.model.arxiv_rev == arxiv_rev)

        return query.all()
