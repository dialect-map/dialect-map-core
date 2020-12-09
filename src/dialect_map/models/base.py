# -*- coding: utf-8 -*-

from abc import abstractmethod
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import ColumnDefault
from sqlalchemy import DateTime
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base


# Base class for all database tables
Base = declarative_base()


class BaseModel:
    """
    Base class for all the Python data models

    Defines class attributes:
        __table__: Table object containing model SQL table information

    Defines object properties:
        id: unique identifier of the data object (abstract)
        json: JSON serialization of the data object
    """

    __table__ = Table()

    def __str__(self) -> str:
        """
        Builds a string representation of the data object
        :return: string representation
        """

        model_class = self.__class__.__name__
        model_fields = []

        for column in self.__table__.columns:
            column_key = column.name
            column_val = getattr(self, column.name)
            model_fields.append(f"{column_key}='{column_val}'")

        return f"<{model_class}({', '.join(model_fields)}>)"

    @property
    @abstractmethod
    def id(self) -> str:
        """
        Gets the unique ID of the data object
        :return: unique ID
        """

        raise NotImplementedError()

    @property
    def data(self) -> dict:
        """
        Gets the data dictionary out of the model object
        :return: data dictionary
        """

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class BaseStaticModel(BaseModel):
    """
    Base class defining key timestamps for keeping track of static models

    Defines tables:
        created_at: when the referenced entity was originally created
        audited_at: when the referenced entity reached the database

    Defines indexes:
        idx_created_at: to query entities by when they were created
    """

    created_at = Column(DateTime, nullable=False, index=True)
    audited_at = Column(DateTime, nullable=True, default=ColumnDefault(datetime.now()))


class BaseEvolvingModel(BaseModel):
    """
    Base class defining key timestamps for keeping track of evolving models

    Defines tables:
        created_at: when the referenced entity was originally created
        updated_at: when the referenced entity was last modified
        audited_at: when the referenced entity reached the database

    Defines indexes:
        idx_created_at: to query entities by when they were created
        idx_updated_at: to query entities  by when they were updated
    """

    created_at = Column(DateTime, nullable=False, index=True)
    updated_at = Column(DateTime, nullable=False, index=True)
    audited_at = Column(DateTime, nullable=True, default=ColumnDefault(datetime.now()))

    @property
    @abstractmethod
    def rev(self) -> int:
        """
        Gets the unique revision of the model
        :return: uniquer revision
        """

        raise NotImplementedError()
