# -*- coding: utf-8 -*-

from .base import StaticController
from ..models import CategoryMembership


class MembershipController(StaticController[CategoryMembership]):
    """
    Controller for the membership objects (static)
    Extend as desired
    """

    model = CategoryMembership
