# -*- coding: utf-8 -*-

from models import CategoryMembership
from storage import BaseDatabase
from .base import BaseController


class MembershipController(BaseController):
    """ Controller for the membership objects """

    def __init__(self, db: BaseDatabase):
        """
        Initializes the controller with the underlying database
        :param db: database engine to use
        """

        self.db = db

    def get(self, id: str) -> CategoryMembership:
        """
        Gets a database record by its ID
        :param id: ID of the database entry
        :return: data object representing the database record
        """

        query = self.db.session.query(CategoryMembership)
        membership = query.get(id)

        if membership is None:
            raise ValueError(f"Unknown membership: {id}")

        return membership

    def create(self, membership: CategoryMembership) -> str:
        """
        Creates a new database record given its object properties
        :param membership: membership object to create the record with
        :return: ID of the created membership
        """

        try:
            self.db.session.add(membership)
            self.db.session.commit()
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        return membership.id

    def delete(self, id: str) -> str:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :return: ID of the deleted membership
        """

        self.db.session.delete(self.get(id))
        self.db.session.commit()
        return id
