# -*- coding: utf-8 -*-

import logging

from ..controllers import *
from ..storage import BaseDatabase
from ..storage import BaseDatabaseContext


logger = logging.getLogger()


class ApplicationService:
    """Service exposing all the model controllers"""

    def __init__(self, db: BaseDatabase, ctx: BaseDatabaseContext):
        """
        Initializes the service with a given database
        :param db: database class to serve as engine
        :param ctx: database context to use as helper
        """

        logger.info("Initializing application service")
        self.db = db
        self.ctx = ctx

    def stop(self):
        """Stops and closes the application service"""

        logger.info("Stopping application service")
        self.db.close_conn()

    @property
    def categories(self) -> CategoryController:
        """Returns an initialized controller for the category model"""
        return CategoryController(db=self.db)

    @property
    def category_memberships(self) -> MembershipController:
        """Returns an initialized controller for the category memberships model"""
        return MembershipController(db=self.db)

    @property
    def jargons(self) -> JargonController:
        """Returns an initialized controller for the jargon model"""
        return JargonController(db=self.db)

    @property
    def jargon_groups(self) -> JargonGroupController:
        """Returns an initialized controller for the jargons group model"""
        return JargonGroupController(db=self.db)

    @property
    def jargon_cat_metrics(self) -> JargonCategoryMetricsController:
        """Returns an initialized controller for the jargon cat. metrics model"""
        return JargonCategoryMetricsController(db=self.db)

    @property
    def jargon_paper_metrics(self) -> JargonPaperMetricsController:
        """Returns an initialized controller for the jargon paper metrics model"""
        return JargonPaperMetricsController(db=self.db)

    @property
    def papers(self) -> PaperController:
        """Returns an initialized controller for the paper model"""
        return PaperController(db=self.db)

    @property
    def paper_authors(self) -> PaperAuthorController:
        """Returns an initialized controller for the paper author model"""
        return PaperAuthorController(db=self.db)

    @property
    def paper_ref_counters(self) -> PaperReferenceCountersController:
        """Returns an initialized controller for the paper ref. counters model"""
        return PaperReferenceCountersController(db=self.db)

    @property
    def paper_refs(self) -> ReferenceController:
        """Returns an initialized controller for the paper reference model"""
        return ReferenceController(db=self.db)
