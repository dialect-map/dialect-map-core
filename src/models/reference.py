# -*- coding: utf-8 -*-

import uuid
from .base import Base
from .base import BaseStaticModel
from sqlalchemy import Column
from sqlalchemy import ForeignKey as FK
from sqlalchemy import String


class PaperReference(Base, BaseStaticModel):
    """
    ArXiv paper - paper reference record.
    Intermediate table to hold paper to paper references.
    """

    __tablename__ = "paper_references"

    id = Column(String(32), default=uuid.uuid4, primary_key=True)
    referenced_paper = Column(String(32), FK("papers.arxiv_id", ondelete="CASCADE"))
    referencing_paper = Column(String(32), FK("papers.arxiv_id", ondelete="CASCADE"))
