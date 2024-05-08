# -*- coding: utf-8 -*-

import re

from datetime import date
from datetime import datetime
from json import JSONDecoder
from json import JSONEncoder

from .base import BaseDecoder
from .base import BaseEncoder


class CustomJSONEncoder(BaseEncoder, JSONEncoder):
    """Custom JSON encoder for Python data types"""

    def __init__(
        self,
        time_resolution: str | None = None,
        time_separation: str | None = None,
        **kwargs,
    ):
        """
        Initializes the custom JSON encoder
        :param time_resolution: resolution for the time objects (optional)
        :param time_separation: separator character for the time objects (optional)
        :param kwargs: additional keyword arguments for the default encoder
        """

        super().__init__(**kwargs)

        if time_resolution is None:
            time_resolution = "seconds"
        if time_separation is None:
            time_separation = " "

        self.time_res = time_resolution
        self.time_sep = time_separation

    def custom_encode(self, obj: object) -> object:
        """
        Encodes a Python object as a JSON valid data type
        :param obj: Python object to encode
        :return: JSON data type
        """

        if isinstance(obj, datetime):
            return obj.isoformat(sep=self.time_sep, timespec=self.time_res)
        elif isinstance(obj, date):
            return obj.isoformat()
        else:
            return self.encode(obj)

    def default(self, obj: object) -> object:
        """
        Encodes a Python object as a JSON valid data type (default function)
        :param obj: Python object to encode
        :return: JSON data type
        """

        return self.custom_encode(obj)


class CustomJSONDecoder(BaseDecoder, JSONDecoder):
    """Custom JSON decoder for Python data types"""

    def __init__(
        self,
        date_regex: str | None = None,
        time_regex: str | None = None,
        **kwargs,
    ):
        """
        Initializes the custom JSON decoder
        :param date_regex: regex to check if the string is a date (optional)
        :param time_regex: regex to check if the string is a time (optional)
        :param kwargs: additional keyword arguments for the default decoder
        """

        super().__init__(**kwargs)

        if date_regex is None:
            date_regex = "[0-9]{4}-[0-9]{2}-[0-9]{2}"
        if time_regex is None:
            time_regex = "[0-9]{2}:[0-9]{2}:[0-9]{2}"

        self.date_regex = f"^{date_regex}$"
        self.datetime_regex = f"^{date_regex}(T| ){time_regex}$"

    def custom_decode(self, obj: object) -> object:
        """
        Decodes a JSON data type as its equivalent Python object
        :param obj: JSON value to decode
        :return: equivalent Python object
        """

        if not isinstance(obj, str):
            return obj

        if re.match(self.date_regex, obj):
            return datetime.strptime(obj, "%Y-%m-%d").date()
        elif re.match(self.datetime_regex, obj):
            return datetime.strptime(obj, "%Y-%m-%d %H:%M:%S")
        else:
            return obj

    def default(self, obj: object) -> object:
        """
        Decodes a JSON data type as its equivalent Python object (default function)
        :param obj: JSON value to decode
        :return: equivalent Python object
        """

        return self.custom_decode(obj)
