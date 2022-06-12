# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .base import Base
from .base import BaseArchivalModel


class Category(Base, BaseArchivalModel):
    """
    ArXiv category information record.
    Contains all the static properties of an ArXiv category
    """

    __tablename__ = "categories"

    category_id = Column(String(32), nullable=False, primary_key=True)
    description = Column(String(256), nullable=False)

    # All main table relationships to child tables. References:
    # Official docs: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
    # Stackoverflow: https://stackoverflow.com/a/38770040
    jargon_metrics = relationship(
        argument="JargonCategoryMetrics",
        backref="jargon_metrics",
        passive_deletes=True,
    )

    @property
    def id(self) -> str:
        """
        Gets the unique ID of the data object
        :return: unique ID
        """

        return self.category_id
