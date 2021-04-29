# -*- coding: utf-8 -*-

from abc import abstractmethod
from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import validates


# Base class for all database tables
Base = declarative_base()


class BaseModel:
    """
    Base class for all the Python data models

    Class attributes:
        __table__: Table object containing model SQL table information

    Object properties:
        data: data dictionary of the data object
        id: unique identifier of the data object (abstract)
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

    @declared_attr
    def created_at(self):
        return Column(DateTime, nullable=False, index=True)

    @declared_attr
    def audited_at(self):
        return Column(DateTime, nullable=True, default=datetime.utcnow)

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
        archived: whether the referenced entity was archived
        created_at: when the referenced entity was originally created
        archived_at: when the referenced entity was last archived
        audited_at: when the referenced entity reached the database

    Indexes:
        idx_created_at: to query entities by when they were created
    """

    @declared_attr
    def archived(self):
        return Column(Boolean, nullable=False, index=False)

    @declared_attr
    def created_at(self):
        return Column(DateTime, nullable=False, index=True)

    @declared_attr
    def archived_at(self):
        return Column(DateTime, nullable=True, index=False)

    @declared_attr
    def audited_at(self):
        return Column(DateTime, nullable=True, index=False, default=datetime.utcnow)

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

    @declared_attr
    def created_at(self):
        return Column(DateTime, nullable=False, index=True)

    @declared_attr
    def updated_at(self):
        return Column(DateTime, nullable=False, index=True)

    @declared_attr
    def audited_at(self):
        return Column(DateTime, nullable=True, default=datetime.utcnow)

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
