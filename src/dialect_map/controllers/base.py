# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod
from datetime import datetime
from typing import Generic
from typing import Tuple
from typing import Type
from typing import TypeVar

from ..models import Base
from ..models import BaseStaticModel
from ..models import BaseArchivalModel
from ..models import BaseEvolvingModel
from ..storage import BaseDatabase


# Generic base model types
StaticModelVar = TypeVar("StaticModelVar", bound=BaseStaticModel)
ArchivalModelVar = TypeVar("ArchivalModelVar", bound=BaseArchivalModel)
EvolvingModelVar = TypeVar("EvolvingModelVar", bound=BaseEvolvingModel)


class BaseController(ABC):
    """ Interface for the data controllers """

    db: BaseDatabase

    @abstractmethod
    def create(self, instance: Base) -> str:
        """
        Creates a new database record given its object properties
        :param instance: data object to create the record from
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

    :attr model:
        Class attribute used to store the data model
        SQLAlchemy will be performing queries against
        (It cannot be obtained at runtime from StaticModelVar)

        For Python 3.8+, remove this attribute and access
        the specific subclass type by using 'typing.get_args'
        Ref: https://docs.python.org/3/library/typing.html#typing.get_args
    """

    model: Type[StaticModelVar]

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

        try:
            query = self.db.session.query(self.model)
            record = query.get(id)
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        if record is None:
            raise ValueError(f"Unknown record: {id}")

        return record

    def create(self, instance: StaticModelVar) -> str:
        """
        Creates a new database record given its object properties
        :param instance: data object to create the record from
        :return: ID of the created object
        """

        try:
            self.db.session.add(instance)
            self.db.session.commit()
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        return instance.id

    def delete(self, id: str) -> str:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :return: ID of the deleted object
        """

        self.db.session.delete(self.get(id))
        self.db.session.commit()
        return id


class ArchivalController(BaseController, Generic[ArchivalModelVar]):
    """
    Controller for the archival models

    :attr model:
        Class attribute used to store the data model
        SQLAlchemy will be performing queries against
        (It cannot be obtained at runtime from ArchivalModelVar)

        For Python 3.8+, remove this attribute and access
        the specific subclass type by using 'typing.get_args'
        Ref: https://docs.python.org/3/library/typing.html#typing.get_args
    """

    model: Type[ArchivalModelVar]

    def __init__(self, db: BaseDatabase):
        """
        Initializes the controller with the underlying database
        :param db: database engine to use
        """

        self.db = db

    def get(self, id: str, include_archived: bool = False) -> ArchivalModelVar:
        """
        Gets a database record by its ID
        :param id: ID of the database entry
        :param include_archived: whether to include archived records
        :return: data object representing the database record
        """

        try:
            query = self.db.session.query(self.model)
            record = query.get(id)
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        if record is None:
            raise ValueError(f"Unknown record: {id}")
        if record.archived is True and include_archived is False:
            raise ValueError(f"The record {id} has been archived")

        return record

    def create(self, instance: ArchivalModelVar) -> str:
        """
        Creates a new database record given its object properties
        :param instance: data object to create the record from
        :return: ID of the created object
        """

        try:
            self.db.session.add(instance)
            self.db.session.commit()
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        return instance.id

    def delete(self, id: str) -> str:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :return: ID of the deleted object
        """

        self.db.session.delete(self.get(id, include_archived=True))
        self.db.session.commit()
        return id

    def archive(self, id: str) -> str:
        """
        Archives a database record by its ID
        :param id: ID of the database entry
        :return: ID of the archived object
        """

        record = self.get(id)
        record.archived = True
        record.archived_at = datetime.utcnow()

        self.db.session.commit()
        return id


class EvolvingController(BaseController, Generic[EvolvingModelVar]):
    """
    Controller for the evolving models

    :attr model:
        Class attribute used to store the data model
        SQLAlchemy will be performing queries against
        (It cannot be obtained at runtime from EvolvingModelVar)

        For Python 3.8+, remove this attribute and access
        the specific subclass type by using 'typing.get_args'
        Ref: https://docs.python.org/3/library/typing.html#typing.get_args
    """

    model: Type[EvolvingModelVar]

    def __init__(self, db: BaseDatabase):
        """
        Initializes the controller with the underlying database
        :param db: database engine to use
        """

        self.db = db

    def get(self, id: str, rev: int) -> EvolvingModelVar:
        """
        Gets a database record by its ID
        :param id: ID of the database entry
        :param rev: revision of the database entry
        :return: data object representing the database record
        """

        try:
            query = self.db.session.query(self.model)
            record = query.get((id, rev))
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        if record is None:
            raise ValueError(f"Unknown record: {id} - Revision: {rev}")

        return record

    def create(self, instance: EvolvingModelVar) -> str:
        """
        Creates a new database record given its object properties
        :param instance: data object to create the record from
        :return: ID of the created object
        """

        try:
            self.db.session.add(instance)
            self.db.session.commit()
        except self.db.session_error as error:
            self.db.session.rollback()
            raise ValueError(error)

        return instance.id

    def delete(self, id: str) -> str:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :return: ID of the deleted object
        """

        rev = 0

        while True:
            try:
                rev += 1
                record = self.get(id, rev)
                self.db.session.delete(record)
            except ValueError:
                break

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
