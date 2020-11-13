# -*- coding: utf-8 -*-

from models import Category
from storage import BaseDatabase
from .base import BaseController


class CategoryController(BaseController):
    """ Controller for the category objects """

    def __init__(self, db: BaseDatabase):
        """
        Initializes the controller with the underlying database
        :param db: database engine to use
        """

        self.db = db

    def get(self, id: str) -> Category:
        """
        Gets a database record by its ID
        :param id: ID of the database entry
        :return: data object representing the database record
        """

        query = self.db.session.query(Category)
        category = query.get(id)

        if category is None:
            raise ValueError(f"Unknown category: {id}")

        return category

    def create(self, category: Category) -> str:
        """
        Creates a new database record given its object properties
        :param category: category object to create the record with
        :return: ID of the created category
        """

        try:
            self.db.session.add(category)
            self.db.session.commit()
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        return category.category_id

    def delete(self, id: str) -> str:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :return: ID of the deleted category
        """

        self.db.session.delete(self.get(id))
        self.db.session.commit()
        return id
