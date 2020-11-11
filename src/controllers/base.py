# -*- coding: utf-8 -*-

from abc import ABCMeta
from abc import abstractmethod
from models import Base
from models import BaseStaticModel
from models import BaseEvolvingModel
from storage import BaseDatabase
from typing import Generic
from typing import Tuple
from typing import TypeVar


# Generic static model type
StaticModelVar = TypeVar("StaticModelVar", bound=BaseStaticModel)

# Generic evolving model type
EvolvingModelVar = TypeVar("EvolvingModelVar", bound=BaseEvolvingModel)


class BaseController(metaclass=ABCMeta):
    """ Interface for the data controllers """

    @abstractmethod
    def create(self, data_object: Base) -> str:
        """
        Creates a new database record given its object properties
        :param data_object: object properties to create the record with
        :return: ID of the created record
        """

        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: str) -> str:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :return: ID of the deleted record
        """

        raise NotImplementedError()


class StaticController(BaseController, Generic[StaticModelVar]):
    """
    Controller for the static models

    :attr data_model:
        Class attribute used to store the data model
        SQLAlchemy will be performing queries against
        (It cannot be obtained at runtime from StaticModelVar)

        For Python 3.8+, remove this attribute and access
        the specific subclass type by using 'typing.get_args'
        Ref: https://docs.python.org/3/library/typing.html#typing.get_args
    """

    data_model: StaticModelVar

    def __init__(self, db: BaseDatabase):
        """
        Initializes the controller with the underlying database
        :param db: database engine to use
        """

        self.db = db

    def get(self, id: str) -> StaticModelVar:
        """
        Gets a database record by its ID
        :param id: ID of the database entry
        :return: data object representing the database record
        """

        query = self.db.session.query(self.data_model)
        record = query.get(id)

        if record is None:
            raise ValueError(f"Unknown record: {id}")

        return record

    def create(self, model: StaticModelVar) -> str:
        """
        Creates a new database record given its object properties
        :param model: model object to create the record with
        :return: ID of the created object
        """

        try:
            self.db.session.add(model)
            self.db.session.commit()
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        return model.id

    def delete(self, id: str) -> str:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :return: ID of the deleted object
        """

        self.db.session.delete(self.get(id))
        self.db.session.commit()
        return id


class EvolvingController(BaseController, Generic[EvolvingModelVar]):
    """
    Controller for the evolving models

    :attr data_model:
        Class attribute used to store the data model
        SQLAlchemy will be performing queries against
        (It cannot be obtained at runtime from StaticModelVar)

        For Python 3.8+, remove this attribute and access
        the specific subclass type by using 'typing.get_args'
        Ref: https://docs.python.org/3/library/typing.html#typing.get_args
    """

    data_model: EvolvingModelVar

    def __init__(self, db: BaseDatabase):
        """
        Initializes the controller with the underlying database
        :param db: database engine to use
        """

        self.db = db

    def get(self, id: str, rev: int = None) -> EvolvingModelVar:
        """
        Gets a database record by its ID
        :param id: ID of the database entry
        :param rev: revision of the database entry (optional)
        :return: data object representing the database record
        """

        if not rev:
            rev = self.data_model.default_rev

        query = self.db.session.query(self.data_model)
        query = query.filter(self.data_model.id == id)
        query = query.filter(self.data_model.rev == rev)
        paper = query.one_or_none()

        if paper is None:
            raise ValueError(f"Unknown paper: {id} - Revision: {rev}")

        return paper

    def create(self, model: EvolvingModelVar) -> str:
        """
        Creates a new database record given its object properties
        :param model: model object to create the record with
        :return: ID of the created object
        """

        try:
            self.db.session.add(model)
            self.db.session.commit()
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        return model.id

    def delete(self, id: str) -> str:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :return: ID of the deleted object
        """

        query = self.db.session.query(self.data_model)
        query = query.filter(self.data_model.id == id)

        self.db.session.delete(query.all())
        self.db.session.commit()
        return id

    def delete_rev(self, id: str, rev: int) -> Tuple[str, int]:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :param rev: revision of the database entry
        :return: ID of the deleted object
        """

        self.db.session.delete(self.get(id, rev))
        self.db.session.commit()
        return id, rev
