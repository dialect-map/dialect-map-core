# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod


class BaseEncoder(ABC):
    """Interface for the Python types encoding classes"""

    @abstractmethod
    def custom_encode(self, obj: object) -> object:
        """
        Encodes a Python object as a basic data type
        :param obj: Python object to encode
        :return: basic type
        """

        raise NotImplementedError()


class BaseDecoder(ABC):
    """Interface for the Python types decoding classes"""

    @abstractmethod
    def custom_decode(self, obj: object) -> object:
        """
        Decodes a basic data type into a Python object
        :param obj: basic value to decode
        :return: equivalent Python object
        """

        raise NotImplementedError()
