# -*- coding: utf-8 -*-

from abc import abstractmethod
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import ColumnDefault
from sqlalchemy import DateTime
from sqlalchemy import Table
from sqlalchemy.orm import validates
from sqlalchemy.ext.declarative import declarative_base

from .__utils import mutable_property


# Base class for all database tables
Base = declarative_base()


class BaseModel:
    """
    Base class for all the Python data models

    Class attributes:
        __table__: Table object containing model SQL table information

    Object properties:
        id: unique identifier of the data object (abstract)
        json: JSON serialization of the data object
    """

    __table__: Table

    def __str__(self) -> str:
        """
        Builds a string representation of the data object
        :return: string representation
        """

        model_class = self.__class__.__name__
        model_fields = []

        for column in self.__table__.columns:
            record = getattr(self, column.name)
            model_fields.append(f"{column.name}='{record}'")

        return f"<{model_class}({', '.join(model_fields)}>)"

    @property
    def data(self) -> dict:
        """
        Gets the data dictionary out of the model object
        :return: data dictionary
        """

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @property
    @abstractmethod
    def id(self) -> str:
        """
        Gets the unique ID of the data object
        :return: unique ID
        """

        raise NotImplementedError()


class BaseStaticModel(BaseModel):
    """
    Base class defining key timestamps for keeping track of static models

    Columns:
        created_at: when the referenced entity was originally created
        audited_at: when the referenced entity reached the database

    Indexes:
        idx_created_at: to query entities by when they were created
    """

    created_at = Column(DateTime, nullable=False, index=True)
    audited_at = Column(DateTime, nullable=True, default=ColumnDefault(datetime.utcnow()))

    @validates("audited_at")
    def check_audited(self, key, val):
        """
        Checks that a private field is not provided by the user
        :param key: targeting column name (unused)
        :param val: provided user value (unused)
        """

        raise ValueError("The column 'audited_at' must not be provided")


class BaseArchivalModel(BaseModel):
    """
    Base class defining key timestamps for keeping track of archival models

    Columns:
        created_at: when the referenced entity was originally created
        archived_at: when the referenced entity was last archived
        audited_at: when the referenced entity reached the database

    Indexes:
        idx_created_at: to query entities by when they were created
    """

    created_at = Column(DateTime, nullable=False, index=True)
    archived_at = Column(DateTime, nullable=True, index=False)
    audited_at = Column(DateTime, nullable=True, default=ColumnDefault(datetime.utcnow()))

    @validates("archived_at")
    def check_archived(self, key, val):
        """
        Checks that a private field is not provided by the user
        :param key: targeting column name (unused)
        :param val: provided user value (unused)
        """

        if not self.archived:
            raise ValueError("The column 'archived_at' must not be provided")

        return val

    @validates("audited_at")
    def check_audited(self, key, val):
        """
        Checks that a private field is not provided by the user
        :param key: targeting column name (unused)
        :param val: provided user value (unused)
        """

        raise ValueError("The column 'audited_at' must not be provided")

    @mutable_property
    @abstractmethod
    def archived(self) -> bool:
        """
        Whether the model was archived or not
        :return: archive status
        """

        raise NotImplementedError()


class BaseEvolvingModel(BaseModel):
    """
    Base class defining key timestamps for keeping track of evolving models

    Columns:
        created_at: when the referenced entity was originally created
        updated_at: when the referenced entity was last modified
        audited_at: when the referenced entity reached the database

    Indexes:
        idx_created_at: to query entities by when they were created
        idx_updated_at: to query entities  by when they were updated
    """

    created_at = Column(DateTime, nullable=False, index=True)
    updated_at = Column(DateTime, nullable=False, index=True)
    audited_at = Column(DateTime, nullable=True, default=ColumnDefault(datetime.utcnow()))

    @validates("audited_at")
    def check_audited(self, key, val):
        """
        Checks that a private field is not provided by the user
        :param key: targeting column name (unused)
        :param val: provided user value (unused)
        """

        raise ValueError("The column 'audited_at' must not be provided")

    @property
    @abstractmethod
    def rev(self) -> int:
        """
        Gets the unique revision of the model
        :return: uniquer revision
        """

        raise NotImplementedError()
