# -*- coding: utf-8 -*-

import uuid
from .base import Base
from .base import BaseStaticModel
from .base import BaseEvolvingModel
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKeyConstraint as FKConstraint
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Paper(Base, BaseEvolvingModel):
    """
    ArXiv paper information record.
    Contains all the static properties of an ArXiv paper
    """

    __tablename__ = "papers"

    arxiv_id = Column(String(32), nullable=False, primary_key=True)
    arxiv_rev = Column(Integer, nullable=False, primary_key=True)
    title = Column(String(256), nullable=False)
    doi_id = Column(String(64), nullable=True)
    url_pdf = Column(String(256), nullable=True)
    url_dvi = Column(String(256), nullable=True)
    url_html = Column(String(256), nullable=True)
    url_latex = Column(String(256), nullable=True)
    url_posts = Column(String(256), nullable=True)
    revision_date = Column(Date, nullable=True)
    submission_date = Column(Date, nullable=False)

    # All main table relationships to child tables. References:
    # Official docs: https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html
    # Stackoverflow: https://stackoverflow.com/a/38770040
    authors = relationship(
        argument="PaperAuthor",
        backref="authors",
        passive_deletes=True,
    )
    ref_counters = relationship(
        argument="PaperReferenceCounters",
        backref="ref_counters",
        passive_deletes=True,
    )
    jargon_metrics = relationship(
        argument="JargonPaperMetrics",
        backref="jargon_metrics",
        passive_deletes=True,
    )

    @property
    def id(self) -> str:
        """ Gets the unique ID of the model """

        return self.arxiv_id

    @property
    def rev(self) -> int:
        """ Gets the unique revision of the model """

        return self.arxiv_rev


class PaperAuthor(Base, BaseStaticModel):
    """
    ArXiv paper author record.
    Contains the information of a single paper author
    """

    __tablename__ = "paper_authors"

    author_id = Column(String(32), default=uuid.uuid4, primary_key=True)
    arxiv_id = Column(String(32), nullable=False)
    arxiv_rev = Column(Integer, nullable=False)
    author_name = Column(String(64), nullable=False)

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

    @property
    def id(self):
        """ Gets the unique ID of the model """

        return self.author_id


class PaperReferenceCounters(Base, BaseStaticModel):
    """
    ArXiv paper reference counters record.
    Contains the number of paper references on a certain date
    """

    __tablename__ = "paper_reference_counters"

    count_id = Column(String(32), default=uuid.uuid4, primary_key=True)
    arxiv_id = Column(String(32), nullable=False)
    arxiv_rev = Column(Integer, nullable=False)
    arxiv_ref_count = Column(Integer, nullable=False)
    total_ref_count = Column(Integer, nullable=False)

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

    @property
    def id(self):
        """ Gets the unique ID of the model """

        return self.count_id
