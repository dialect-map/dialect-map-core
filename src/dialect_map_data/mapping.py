# -*- coding: utf-8 -*-

from pathlib import Path

from dialect_map.models import Category
from dialect_map.models import Jargon
from dialect_map.models import JargonCategoryMetrics
from dialect_map.models import JargonPaperMetrics
from dialect_map.models import CategoryMembership
from dialect_map.models import Paper
from dialect_map.models import PaperAuthor
from dialect_map.models import PaperReference
from dialect_map.models import PaperReferenceCounters


# Get the tests folder absolute path
FILES_PATH = Path(__file__).parent.joinpath("files")


# Define a relationship between data files and models
FILES_MAPPINGS = [
    {
        "file": FILES_PATH.joinpath("test_category.json"),
        "model": Category,
    },
    {
        "file": FILES_PATH.joinpath("test_jargon.json"),
        "model": Jargon,
    },
    {
        "file": FILES_PATH.joinpath("test_jargon_cat_metrics.json"),
        "model": JargonCategoryMetrics,
    },
    {
        "file": FILES_PATH.joinpath("test_jargon_paper_metrics.json"),
        "model": JargonPaperMetrics,
    },
    {
        "file": FILES_PATH.joinpath("test_membership.json"),
        "model": CategoryMembership,
    },
    {
        "file": FILES_PATH.joinpath("test_paper.json"),
        "model": Paper,
    },
    {
        "file": FILES_PATH.joinpath("test_paper_author.json"),
        "model": PaperAuthor,
    },
    {
        "file": FILES_PATH.joinpath("test_paper_ref.json"),
        "model": PaperReference,
    },
    {
        "file": FILES_PATH.joinpath("test_paper_ref_counters.json"),
        "model": PaperReferenceCounters,
    },
]
