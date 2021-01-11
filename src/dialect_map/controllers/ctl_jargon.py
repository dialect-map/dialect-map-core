# -*- coding: utf-8 -*-

from .base import StaticController
from ..models import Jargon


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
