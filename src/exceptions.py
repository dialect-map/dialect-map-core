# -*- coding: utf-8 -*-

import logging
from flask import jsonify
from flask import make_response

logger = logging.getLogger()


def not_found_request(error: Exception):
    """
    Exception handler for requests that raise a ValueError because there is no results
    :param error: exception object that has been raised
    :return: HTTP 400 response
    """

    logger.error(f"Request error: {error}")
    return make_response(jsonify({"message": str(error)}), 400)


def internal_error(error):
    """
    Exception handler for requests that raise a not caught exception
    :param error: exception object that has been raised
    :return: HTTP 500 response
    """

    logger.error(f"Internal error: {error}")
    return make_response(jsonify({"message": str(error)}), 500)
