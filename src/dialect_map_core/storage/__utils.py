# -*- coding: utf-8 -*-

from .database import BaseDatabaseError
from .database import SQLAlchemyError


def get_error_message(error: BaseDatabaseError) -> str:
    """
    Gets the error message out of a library exception class
    :param error: Database error object
    :return: Database error message
    """

    # SQLAlchemy specific: unwrap the original error
    if isinstance(error, SQLAlchemyError):
        error = getattr(error, "orig")

    error_type = str(error.__class__.__name__)
    error_msg = str(error)

    return f"{error_type}: {error_msg}"
