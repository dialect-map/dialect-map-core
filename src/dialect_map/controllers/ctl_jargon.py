# -*- coding: utf-8 -*-

from sqlalchemy import false

from .base import ArchivalController
from ..models import Jargon
from ..models import JargonGroup


class JargonController(ArchivalController[Jargon]):
    """
    Controller for the jargon objects (archival)
    Extend as desired
    """

    model = Jargon

    def get_by_string(self, jargon_term: str) -> Jargon:
        """
        Gets a database record by its string value
        :param jargon_term: jargon string representation
        :return: jargon term object
        """

        query = self.db.session.query(self.model)
        query = query.filter(self.model.archived == false())
        query = query.filter(self.model.jargon_term == jargon_term)

        return query.one_or_none()

    def get_by_group(self, group_id: str) -> list:
        """
        Gets a database set of jargons given their group ID
        :param group_id: jargon group ID to filter by
        :return: list of jargon terms
        """

        group = self.db.session.query(JargonGroup)
        group = group.filter(JargonGroup.archived == false())
        group = group.filter(JargonGroup.group_id == group_id)

        group = group.one_or_none()
        jargons = []

        if group:
            query = self.db.session.query(self.model)
            query = query.filter(self.model.archived == false())
            query = query.filter(self.model.group_id == group_id)
            jargons = query.all()

        return jargons


class JargonGroupController(ArchivalController[JargonGroup]):
    """
    Controller for the jargon group objects (archival)
    Extend as desired
    """

    model = JargonGroup
