# -*- coding: utf-8 -*-

import uuid
from .base import Base
from .base import BaseStaticModel
from sqlalchemy import Column
from sqlalchemy import ForeignKey as FK
from sqlalchemy import ForeignKeyConstraint as FKConstraint
from sqlalchemy import String


class CategoryMembership(Base, BaseStaticModel):
    """
    ArXiv paper - category membership record.
    Intermediate table to relate papers to categories
    """

    __tablename__ = "paper_categories"

    id = Column(String(32), default=uuid.uuid4, primary_key=True)
    arxiv_id = Column(String(32), nullable=False)
    arxiv_rev = Column(String(32), nullable=False)
    category_id = Column(String(32), FK("categories.category_id", ondelete="CASCADE"))

    # Define a Foreign key over multiple columns (Composite Foreign Key)
    # Official docs: https://docs.sqlalchemy.org/en/13/core/constraints.html
    # Stackoverflow: https://stackoverflow.com/a/7506168
    __table_args__ = (
        FKConstraint(
            columns=("arxiv_id", "arxiv_rev"),
            refcolumns=("papers.arxiv_id", "papers.arxiv_rev"),
            ondelete="CASCADE",
        ),
    )
