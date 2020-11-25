# -*- coding: utf-8 -*-

from .routes_category import bp as blueprint_category
from .routes_jargon import bp as blueprint_jargon
from .routes_membership import bp as blueprint_membership
from .routes_metrics import bp as blueprint_metrics
from .routes_paper import bp as blueprint_paper
from .routes_reference import bp as blueprint_reference


all_blueprints = [
    blueprint_category,
    blueprint_jargon,
    blueprint_membership,
    blueprint_metrics,
    blueprint_paper,
    blueprint_reference,
]
