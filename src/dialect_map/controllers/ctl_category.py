# -*- coding: utf-8 -*-

from .base import StaticController
from ..models import Category


class CategoryController(StaticController[Category]):
    """
    Controller for the Category objects (static)
    Extend as desired
    """

    model = Category
