# -*- coding: utf-8 -*-

from abc import abstractmethod
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import ColumnDefault
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base


# Base class for all database tables
Base = declarative_base()


class BaseStaticModel:
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

    def __str__(self) -> str:
        """
        Builds a string representation of the object
        avoiding SQLAlchemy internal attributes
        """

        fields = ", ".join(
            f"{key}='{value}'"
            for key, value in self.__dict__.items()
            if key.startswith("_") is False
        )

        return f"<{self.__class__.__name__}({fields})>"

    @property
    @abstractmethod
    def id(self) -> str:
        """ Gets the unique ID of the model """

        raise NotImplementedError()


class BaseEvolvingModel:
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

    def __str__(self) -> str:
        """
        Builds a string representation of the object
        avoiding SQLAlchemy internal attributes
        """

        fields = ", ".join(
            f"{key}='{value}'"
            for key, value in self.__dict__.items()
            if key.startswith("_") is False
        )

        return f"<{self.__class__.__name__}({fields})>"

    @property
    @abstractmethod
    def id(self) -> str:
        """ Gets the unique ID of the model """

        raise NotImplementedError()

    @property
    @abstractmethod
    def rev(self) -> int:
        """ Gets the unique revision of the model """

        raise NotImplementedError()
