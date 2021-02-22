# -*- coding: utf-8 -*-

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKeyConstraint as FKConstraint
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .base import Base
from .base import BaseStaticModel
from .base import BaseArchivalModel
from .__utils import generate_id


class Jargon(Base, BaseArchivalModel):
    """
    Jargon term related information record.
    Contains all the static properties of a jargon term
    """

    __tablename__ = "jargons"

    jargon_id = Column(String(32), default=generate_id, primary_key=True)
    jargon_str = Column(String(64), nullable=False, index=True)
    jargon_regex = Column(String(128), nullable=False)
    group_id = Column(String(32), nullable=True)
    archived = Column(Boolean, nullable=False)
    num_words = Column(Integer, nullable=False)

    __table_args__ = (
        FKConstraint(
            columns=("group_id",),
            refcolumns=("jargon_groups.group_id",),
            ondelete="CASCADE",
        ),
    )

    # All main table relationships to child tables. References:
    # Official docs: https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html
    # Stackoverflow: https://stackoverflow.com/a/38770040
    category_metrics = relationship(
        argument="JargonCategoryMetrics",
        backref="category_metrics",
        passive_deletes=True,
    )
    paper_metrics = relationship(
        argument="JargonPaperMetrics",
        backref="paper_metrics",
        passive_deletes=True,
    )

    @property
    def id(self) -> str:
        """
        Gets the unique ID of the data object
        :return: unique ID
        """

        return self.jargon_id


class JargonGroup(Base, BaseStaticModel):
    """
    Jargon group to relate jargons with similar meaning.
    Contains all the static properties of a jargon group
    """

    __tablename__ = "jargon_groups"

    group_id = Column(String(32), default=generate_id, primary_key=True)
    description = Column(String(256), nullable=False)

    # All main table relationships to child tables. References:
    # Official docs: https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html
    # Stackoverflow: https://stackoverflow.com/a/38770040
    jargons = relationship(
        argument="Jargon",
        backref="jargons",
        passive_deletes=True,
    )

    @property
    def id(self) -> str:
        """
        Gets the unique ID of the data object
        :return: unique ID
        """

        return self.group_id
