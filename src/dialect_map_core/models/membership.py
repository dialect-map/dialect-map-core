# -*- coding: utf-8 -*-

from sqlalchemy import ForeignKeyConstraint as FKConstraint
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapped_column as Column

from .base import Base
from .base import BaseStaticModel
from .__utils import generate_id


class CategoryMembership(Base, BaseStaticModel):
    """
    ArXiv paper - category membership record.
    Intermediate table to relate papers to categories
    """

    __tablename__ = "category_memberships"

    membership_id = Column(String(32), nullable=False, primary_key=True, default=generate_id)
    arxiv_id = Column(String(32), nullable=False)
    arxiv_rev = Column(Integer, nullable=False)
    category_id = Column(String(32), nullable=False)

    # Define a Foreign key over multiple columns (Composite Foreign Key)
    # Official docs: https://docs.sqlalchemy.org/en/20/core/constraints.html
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
        UniqueConstraint("arxiv_id", "arxiv_rev", "category_id"),
    )

    @property
    def id(self) -> str:
        """
        Gets the unique ID of the data object
        :return: unique ID
        """

        return self.membership_id
