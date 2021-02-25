# -*- coding: utf-8 -*-

from .base import ArchivalController
from ..models import Jargon
from ..models import JargonGroup


class JargonController(ArchivalController[Jargon]):
    """
    Controller for the jargon objects (archival)
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
        query = query.filter(self.model.archived.is_(False))

        return query.one_or_none()

    def get_by_group(self) -> list:
        """
        Gets a database jargon records grouped
        :return: list of jargon term groups
        """

        groups = self.db.session.query(JargonGroup)
        groups = groups.filter(JargonGroup.archived.is_(False))

        group_ids = [g.id for g in groups]
        grouped = []

        for id in group_ids:
            query = self.db.session.query(self.model)
            query = query.filter(self.model.group_id == id)
            query = query.filter(self.model.archived.is_(False))
            grouped.append(query.all())

        return grouped


class JargonGroupController(ArchivalController[JargonGroup]):
    """
    Controller for the jargon group objects (archival)
    Extend as desired
    """

    model = JargonGroup
