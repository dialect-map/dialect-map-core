# -*- coding: utf-8 -*-

from pathlib import Path
from typing import NamedTuple
from typing import Type

from dialect_map.models import Category
from dialect_map.models import Jargon
from dialect_map.models import JargonCategoryMetrics
from dialect_map.models import JargonPaperMetrics
from dialect_map.models import CategoryMembership
from dialect_map.models import Paper
from dialect_map.models import PaperAuthor
from dialect_map.models import PaperReference
from dialect_map.models import PaperReferenceCounters


class Mapping(NamedTuple):
    """ Mapping between file data records and their associated data model """

    file: str
    model: Type


FILES_PATH = Path(__file__).parent.joinpath("files")


### NOTE:
### Mappings order matters, as there are some data models
### that define Foreign key constrains on other data models.
FILES_MAPPINGS = [
    Mapping(
        file=str(FILES_PATH.joinpath("test_category.json")),
        model=Category,
    ),
    Mapping(
        file=str(FILES_PATH.joinpath("test_jargon.json")),
        model=Jargon,
    ),
    Mapping(
        file=str(FILES_PATH.joinpath("test_paper.json")),
        model=Paper,
    ),
    Mapping(
        file=str(FILES_PATH.joinpath("test_membership.json")),
        model=CategoryMembership,
    ),
    Mapping(
        file=str(FILES_PATH.joinpath("test_jargon_cat_metrics.json")),
        model=JargonCategoryMetrics,
    ),
    Mapping(
        file=str(FILES_PATH.joinpath("test_jargon_paper_metrics.json")),
        model=JargonPaperMetrics,
    ),
    Mapping(
        file=str(FILES_PATH.joinpath("test_paper_author.json")),
        model=PaperAuthor,
    ),
    Mapping(
        file=str(FILES_PATH.joinpath("test_paper_ref.json")),
        model=PaperReference,
    ),
    Mapping(
        file=str(FILES_PATH.joinpath("test_paper_ref_counters.json")),
        model=PaperReferenceCounters,
    ),
]
