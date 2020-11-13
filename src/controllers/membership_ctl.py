# -*- coding: utf-8 -*-

from models import CategoryMembership
from .base import StaticController


class MembershipController(StaticController[CategoryMembership]):
    """
    Controller for the membership objects (static)
    Extend as desired
    """

    data_model = CategoryMembership
