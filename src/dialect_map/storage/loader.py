# -*- coding: utf-8 -*-

import json
from abc import ABC
from abc import abstractmethod

from ..encoding import CustomJSONDecoder


class BaseFileLoader(ABC):
    """Interface for the data file loader classes"""

    @abstractmethod
    def load(self, file_path: str) -> list:
        """
        Loads a specific file of data objects into memory
        :param file_path: path to the specific file to load
        :return: list of dictionary records
        """

        raise NotImplementedError()


class JSONFileLoader(BaseFileLoader):
    """Data file loader class for JSON documents"""

    def __init__(self, **kwargs):
        """
        Initialized the JSON data file loader
        :param kwargs: arguments for the JSON decoder
        """

        self.decoder = CustomJSONDecoder(**kwargs)

    def load(self, file_path: str) -> list:
        """
        Loads a specific JSON records file into memory
        :param file_path: path to the specific JSON file to load
        :return: list of dictionary records
        """

        with open(file_path) as file:
            records = json.load(file)

        if type(records) != list:
            records = [records]

        # Decode strings into corresponding Python objects
        for record in records:
            for key, val in record.items():
                record[key] = self.decoder.custom_decode(val)

        return records
