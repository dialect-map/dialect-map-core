# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod
from datetime import datetime
from typing import Generic
from typing import List
from typing import Tuple
from typing import Type
from typing import TypeVar

from sqlalchemy import false

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
    """Interface for the data controllers"""

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
            record = self.db.session.get(self.model, id)
        except Exception:
            self.db.session.rollback()
            raise

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
        except Exception:
            self.db.session.rollback()
            raise

        return instance.id

    def create_all(self, instances: List[StaticModelVar]) -> int:
        """
        Creates new database records given a list of objects
        :param instances: data objects to create the records from
        :return: number of successfully create records
        """

        try:
            self.db.session.add_all(instances)
            self.db.session.commit()
        except Exception:
            self.db.session.rollback()
            raise

        return len(instances)

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
            record = self.db.session.get(self.model, id)
        except Exception:
            self.db.session.rollback()
            raise

        if record is None:
            raise ValueError(f"Unknown record: {id}")
        if record.archived is True and include_archived is False:
            raise ValueError(f"The record {id} has been archived")

        return record

    def get_all(self, include_archived: bool = False) -> list:
        """
        Gets all database records
        :param include_archived: whether to include archived records
        :return: list of records
        """

        query = self.db.session.query(self.model)

        if include_archived is False:
            query = query.filter(self.model.archived == false())

        return query.all()

    def create(self, instance: ArchivalModelVar) -> str:
        """
        Creates a new database record given its object properties
        :param instance: data object to create the record from
        :return: ID of the created object
        """

        try:
            self.db.session.add(instance)
            self.db.session.commit()
        except Exception:
            self.db.session.rollback()
            raise

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
            record = self.db.session.get(self.model, (id, rev))
        except Exception:
            self.db.session.rollback()
            raise

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
        except Exception:
            self.db.session.rollback()
            raise

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
