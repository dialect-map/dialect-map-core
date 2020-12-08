# -*- coding: utf-8 -*-

from abc import ABCMeta
from abc import abstractmethod
from typing import Any


class BaseParser(metaclass=ABCMeta):
    """ Interface for parsing strings into Python types """

    @abstractmethod
    def check(self, value: Any) -> bool:
        """
        Checks if a particular string value matches the parsing data type
        :param value: value to check
        :return: whether the value matches
        """

        raise NotImplementedError()

    @abstractmethod
    def parse(self, value: str) -> object:
        """
        Parses a string and transforms it into the corresponding Python object
        :param value: string to parse
        :return: Python object
        """

        raise NotImplementedError()
