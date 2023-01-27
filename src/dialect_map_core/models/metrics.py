# -*- coding: utf-8 -*-

from sqlalchemy import Float
from sqlalchemy import ForeignKeyConstraint as FKConstraint
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import mapped_column as Column

from .base import Base
from .base import StaticModel
from .__utils import generate_id


class JargonCategoryMetrics(Base, StaticModel):
    """
    ArXiv category jargon NLP metrics
    Contains every NLP metric information computable for a jargon term.
    """

    __tablename__ = "jargon_category_metrics"

    metric_id = Column(String(32), nullable=False, primary_key=True, default=generate_id)
    jargon_id = Column(String(32), nullable=False, index=True)
    category_id = Column(String(32), nullable=False)
    abs_freq = Column(Integer, nullable=False)
    rel_freq = Column(Float, nullable=False)

    __table_args__ = (
        FKConstraint(
            columns=("jargon_id",),
            refcolumns=("jargons.jargon_id",),
            ondelete="CASCADE",
        ),
        FKConstraint(
            columns=("category_id",),
            refcolumns=("categories.category_id",),
            ondelete="CASCADE",
        ),
    )

    @property
    def id(self) -> str:
        """
        Gets the unique ID of the data object
        :return: unique ID
        """

        return self.metric_id


class JargonPaperMetrics(Base, StaticModel):
    """
    ArXiv paper jargon NLP metrics
    Contains every NLP metric information computable for a jargon term.
    """

    __tablename__ = "jargon_paper_metrics"

    metric_id = Column(String(32), nullable=False, primary_key=True, default=generate_id)
    jargon_id = Column(String(32), nullable=False, index=True)
    arxiv_id = Column(String(32), nullable=False)
    arxiv_rev = Column(Integer, nullable=False)
    abs_freq = Column(Integer, nullable=False)
    rel_freq = Column(Float, nullable=False)

    # Define a Foreign key over multiple columns (Composite Foreign Key)
    # Official docs: https://docs.sqlalchemy.org/en/20/core/constraints.html
    # Stackoverflow: https://stackoverflow.com/a/7506168
    __table_args__ = (
        FKConstraint(
            columns=("jargon_id",),
            refcolumns=("jargons.jargon_id",),
            ondelete="CASCADE",
        ),
        FKConstraint(
            columns=("arxiv_id", "arxiv_rev"),
            refcolumns=("papers.arxiv_id", "papers.arxiv_rev"),
            ondelete="CASCADE",
        ),
    )

    @property
    def id(self) -> str:
        """
        Gets the unique ID of the data object
        :return: unique ID
        """

        return self.metric_id
