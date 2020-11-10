# -*- coding: utf-8 -*-

import uuid
from .base import Base
from .base import BaseStaticModel
from .base import BaseEvolvingModel
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey as FK
from sqlalchemy import ForeignKeyConstraint as FKConstraint
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Jargon(Base, BaseStaticModel):
    """
    Jargon term related information record.
    Contains all the static properties of a jargon term
    """

    __tablename__ = "jargons"

    jargon_id = Column(String(32), default=uuid.uuid4, primary_key=True)
    jargon_str = Column(String(64), nullable=False, index=True)
    num_words = Column(Integer, nullable=False)

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


class JargonCategoryMetrics(Base, BaseEvolvingModel):
    """
    ArXiv category jargon NLP metrics
    Contains every NLP metric information computable for a jargon term.
    """

    __tablename__ = "jargon_category_metrics"

    metric_id = Column(String(32), default=uuid.uuid4, primary_key=True)
    jargon_id = Column(String(32), FK("jargons.jargon_id", ondelete="CASCADE"))
    category_id = Column(String(32), FK("categories.category_id", ondelete="CASCADE"))
    abs_freq = Column(Integer, nullable=False)
    rel_freq = Column(Float, nullable=False)


class JargonPaperMetrics(Base, BaseEvolvingModel):
    """
    ArXiv paper jargon NLP metrics
    Contains every NLP metric information computable for a jargon term.
    """

    __tablename__ = "jargon_paper_metrics"

    metric_id = Column(String(32), default=uuid.uuid4, primary_key=True)
    jargon_id = Column(String(32), FK("jargons.jargon_id", ondelete="CASCADE"))
    arxiv_id = Column(String(32), nullable=False)
    arxiv_rev = Column(String(32), nullable=False)
    abs_freq = Column(Integer, nullable=False)
    rel_freq = Column(Float, nullable=False)

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
