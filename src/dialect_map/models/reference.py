# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import ForeignKeyConstraint as FKConstraint
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

from .base import Base
from .base import BaseStaticModel
from .__utils import generate_id


class PaperReference(Base, BaseStaticModel):
    """
    ArXiv paper - paper reference record.
    Intermediate table to hold paper to paper references.
    """

    __tablename__ = "paper_references"

    reference_id = Column(String(32), default=generate_id, primary_key=True)
    source_arxiv_id = Column(String(32), nullable=False)
    source_arxiv_rev = Column(Integer, nullable=False)
    target_arxiv_id = Column(String(32), nullable=False)
    target_arxiv_rev = Column(Integer, nullable=False)

    # Define a Foreign key over multiple columns (Composite Foreign Key)
    # Official docs: https://docs.sqlalchemy.org/en/13/core/constraints.html
    # Stackoverflow: https://stackoverflow.com/a/7506168
    __table_args__ = (
        FKConstraint(
            columns=("source_arxiv_id", "source_arxiv_rev"),
            refcolumns=("papers.arxiv_id", "papers.arxiv_rev"),
            ondelete="CASCADE",
        ),
        FKConstraint(
            columns=("target_arxiv_id", "target_arxiv_rev"),
            refcolumns=("papers.arxiv_id", "papers.arxiv_rev"),
            ondelete="CASCADE",
        ),
        UniqueConstraint(
            "source_arxiv_id", "source_arxiv_rev", "target_arxiv_id", "target_arxiv_rev"
        ),
    )

    @property
    def id(self) -> str:
        """
        Gets the unique ID of the data object
        :return: unique ID
        """

        return self.reference_id
