# -*- coding: utf-8 -*-

from models import Category
from .base import StaticController


class CategoryController(StaticController[Category]):
    """
    Controller for the Category objects (static)
    Extend as desired
    """

    model = Category
