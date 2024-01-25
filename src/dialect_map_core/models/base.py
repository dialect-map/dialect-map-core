# -*- coding: utf-8 -*-

from abc import abstractmethod

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.orm import ONETOMANY
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import mapped_column as Column
from sqlalchemy.orm import validates

from .__utils import generate_timestamp


class Base(DeclarativeBase):
    """Base class for all the Python data models"""

    def __init__(self, **kwargs):
        """
        Custom initializer that allows nested children initialization.
        Only keys that are present as instance's class attributes are allowed.
        These could be, for example, any mapped columns or relationships.

        Code inspired from GitHub.
        Ref: https://github.com/tiangolo/fastapi/issues/2194
        """

        super().__init__()

        cls = self.__class__
        model_columns = self.__mapper__.columns
        relationships = self.__mapper__.relationships

        for key, val in kwargs.items():
            if not hasattr(cls, key):
                raise TypeError(f"Invalid keyword argument: {key}")

            if key in model_columns:
                setattr(self, key, val)
                continue

            if key in relationships:
                relation_dir = relationships[key].direction.name
                relation_cls = relationships[key].mapper.entity

                if relation_dir == ONETOMANY.name:
                    instances = [relation_cls(**elem) for elem in val]
                    setattr(self, key, instances)

    def __str__(self) -> str:
        """
        Builds a string representation of the data object
        :return: string representation
        """

        model_name = self.__class__.__name__
        model_cols = self.__table__.columns.keys()
        obj_values = []

        for col in model_cols:
            val = getattr(self, col)
            obj_values.append(f"{col}='{val}'")

        return f"<{model_name}({', '.join(obj_values)}>)"


class StaticModel:
    """
    Mixin class defining key timestamps for keeping track of static models

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
        return Column(DateTime, nullable=True, index=False, default=generate_timestamp)

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
    def id(self) -> str:
        """
        Gets the unique ID of the data object
        :return: unique ID
        """

        raise NotImplementedError()


class ArchivalModel:
    """
    Mixin class defining key timestamps for keeping track of archival models

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
        return Column(DateTime, nullable=True, index=False, default=generate_timestamp)

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

    @property
    @abstractmethod
    def id(self) -> str:
        """
        Gets the unique ID of the data object
        :return: unique ID
        """

        raise NotImplementedError()


class EvolvingModel:
    """
    Mixin class defining key timestamps for keeping track of evolving models

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
        return Column(DateTime, nullable=False, index=True, onupdate=generate_timestamp)

    @declared_attr
    def audited_at(self):
        return Column(DateTime, nullable=True, index=False, default=generate_timestamp)

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
    def id(self) -> str:
        """
        Gets the unique ID of the data object
        :return: unique ID
        """

        raise NotImplementedError()

    @property
    @abstractmethod
    def rev(self) -> int:
        """
        Gets the unique revision of the model
        :return: uniquer revision
        """

        raise NotImplementedError()
