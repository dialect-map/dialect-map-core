# -*- coding: utf-8 -*-

from .base import ArchivalController
from ..models import Category


class CategoryController(ArchivalController[Category]):
    """
    Controller for the Category objects (archival)
    Extend as desired
    """

    model = Category
