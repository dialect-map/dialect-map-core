# -*- coding: utf-8 -*-

import re
from datetime import date
from datetime import datetime
from json import JSONDecoder
from json import JSONEncoder
from typing import Any

from .base import BaseDecoder
from .base import BaseEncoder


class CustomJSONEncoder(BaseEncoder, JSONEncoder):
    """Custom JSON encoder for Python data types"""

    def __init__(self, time_res: str = None, time_sep: str = None, **kwargs):
        """
        Initializes the custom JSON encoder
        :param time_res: time resolution for the time objects
        :param time_sep: time separator character for the time objects
        :param kwargs: additional keyword arguments for the default encoder
        """

        super().__init__(**kwargs)

        if time_res is None:
            time_res = "seconds"
        if time_sep is None:
            time_sep = " "

        self.time_res = time_res
        self.time_sep = time_sep

    def custom_encode(self, obj: Any) -> Any:
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

    def default(self, obj: Any) -> Any:
        """
        Encodes a Python object as a JSON valid data type (default function)
        :param obj: Python object to encode
        :return: JSON data type
        """

        return self.custom_encode(obj)


class CustomJSONDecoder(BaseDecoder, JSONDecoder):
    """Custom JSON decoder for Python data types"""

    def __init__(self, date_regex: str = None, datetime_regex: str = None, **kwargs):
        """
        Initializes the custom JSON decoder
        :param date_regex: regex to check if the string is a date
        :param datetime_regex: regex to check if the string is a datetime
        :param kwargs: additional keyword arguments for the default decoder
        """

        super().__init__(**kwargs)

        date_format = "[0-9]{4}-[0-9]{2}-[0-9]{2}"
        time_format = "[0-9]{2}:[0-9]{2}:[0-9]{2}"

        if date_regex is None:
            date_regex = f"^{date_format}$"
        if datetime_regex is None:
            datetime_regex = f"^{date_format}(T| ){time_format}$"

        self.date_regex = date_regex
        self.datetime_regex = datetime_regex

    def _check_date(self, value: str) -> bool:
        """
        Checks if a particular string matches the date format
        :param value: string to check
        :return: whether it is a date
        """

        if re.match(self.date_regex, value):
            return True

        return False

    def _check_datetime(self, value: str) -> bool:
        """
        Checks if a particular string matches the datetime format
        :param value: string to check
        :return: whether it is a datetime
        """

        if re.match(self.datetime_regex, value):
            return True

        return False

    def custom_decode(self, obj: Any) -> Any:
        """
        Decodes a JSON data type as its equivalent Python object
        :param obj: JSON value to decode
        :return: equivalent Python object
        """

        if not isinstance(obj, str):
            return obj

        if self._check_date(obj):
            return datetime.strptime(obj, "%Y-%m-%d").date()
        elif self._check_datetime(obj):
            return datetime.strptime(obj, "%Y-%m-%d %H:%M:%S")
        else:
            return obj

    def default(self, obj: Any) -> Any:
        """
        Decodes a JSON data type as its equivalent Python object (default function)
        :param obj: JSON value to decode
        :return: equivalent Python object
        """

        return self.custom_decode(obj)
