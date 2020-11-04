# -*- coding: utf-8 -*-

import uuid
from .base import Base
from .base import BaseEvolvingModel
from sqlalchemy import Column
from sqlalchemy import ForeignKey as FK
from sqlalchemy import String


class CategoryMembership(Base, BaseEvolvingModel):
    """
    ArXiv paper - category membership record.
    Intermediate table to relate papers to categories
    """

    __tablename__ = "paper_categories"

    id = Column(String(32), default=uuid.uuid4, primary_key=True)
    arxiv_id = Column(String(32), FK("papers.arxiv_id", ondelete="CASCADE"))
    category_id = Column(String(32), FK("categories.category_id", ondelete="CASCADE"))
