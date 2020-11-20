# -*- coding: utf-8 -*-

import re
from datetime import datetime
from typing import Any
from .base import BaseParser


class DatetimeParser(BaseParser):
    """ Parser class to parse string date times """

    def __init__(self, datetime_format: str = None, datetime_regex: str = None):
        """
        Initializes the string datetime parser using the desired format and regex
        :param datetime_format: format to parse the string into
        :param datetime_regex: expression to detect if the string is a date
        """

        if datetime_format is None:
            datetime_format = "%Y-%m-%d %H:%M:%S"

        if datetime_regex is None:
            datetime_regex = "^[0-9]{4}-[0-9]{2}-[0-9]{2}(T| )[0-9]{2}:[0-9]{2}:[0-9]{2}$"

        self.datetime_format = datetime_format
        self.datetime_regex = datetime_regex

    def check(self, value: Any) -> bool:
        """
        Checks if a particular string value matches the datetime format
        :param value: value to check
        :return: whether the value is a datetime
        """

        if not isinstance(value, str):
            return False

        if not re.match(self.datetime_regex, value):
            return False

        return True

    def parse(self, value: str) -> datetime:
        """
        Parses a string and transforms it into the corresponding Python datetime
        :param value: string to parse
        :return: Python datetime
        """

        return datetime.strptime(value, self.datetime_format)
