# -*- coding: utf-8 -*-

import re
from datetime import date
from datetime import datetime
from typing import Any
from .base import BaseParser


class DateParser(BaseParser):
    """ Parser class to parse string dates """

    def __init__(self, date_format: str = None, date_regex: str = None):
        """
        Initializes the string date parser using the desired format and regex
        :param date_format: format to parse the string into
        :param date_regex: expression to detect if the string is a date
        """

        if date_format is None:
            date_format = "%Y-%m-%d"

        if date_regex is None:
            date_regex = "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"

        self.date_format = date_format
        self.date_regex = date_regex

    def check(self, value: Any) -> bool:
        """
        Checks if a particular string value matches the date format
        :param value: value to check
        :return: whether the value is a date
        """

        if not isinstance(value, str):
            return False

        if not re.match(self.date_regex, value):
            return False

        return True

    def parse(self, value: str) -> date:
        """
        Parses a string and transforms it into the corresponding Python object
        :param value: string to parse
        :return: Python date
        """

        return datetime.strptime(value, self.date_format).date()
