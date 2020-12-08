# -*- coding: utf-8 -*-

import uuid
from sqlalchemy import Column
from sqlalchemy import ForeignKeyConstraint as FKConstraint
from sqlalchemy import Integer
from sqlalchemy import String

from .base import Base
from .base import BaseStaticModel


class CategoryMembership(Base, BaseStaticModel):
    """
    ArXiv paper - category membership record.
    Intermediate table to relate papers to categories
    """

    __tablename__ = "paper_categories"

    membership_id = Column(String(32), default=uuid.uuid4, primary_key=True)
    arxiv_id = Column(String(32), nullable=False)
    arxiv_rev = Column(Integer, nullable=False)
    category_id = Column(String(32), nullable=False)

    # Define a Foreign key over multiple columns (Composite Foreign Key)
    # Official docs: https://docs.sqlalchemy.org/en/13/core/constraints.html
    # Stackoverflow: https://stackoverflow.com/a/7506168
    __table_args__ = (
        FKConstraint(
            columns=("arxiv_id", "arxiv_rev"),
            refcolumns=("papers.arxiv_id", "papers.arxiv_rev"),
            ondelete="CASCADE",
        ),
        FKConstraint(
            columns=("category_id",),
            refcolumns=("categories.category_id",),
            ondelete="CASCADE",
        ),
    )

    @property
    def id(self):
        """ Gets the unique ID of the model """

        return self.membership_id
