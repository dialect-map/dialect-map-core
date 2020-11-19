# -*- coding: utf-8 -*-

import json
from abc import ABCMeta
from abc import abstractmethod
from parsers import BaseParser
from typing import List


class BaseLoader(metaclass=ABCMeta):
    """ Interface for the data loader classes """

    @abstractmethod
    def load(self, file_path: str) -> list:
        """
        Loads a specific file of data objects into memory
        :param file_path: path to the specific file to load
        """

        raise NotImplementedError()


class JsonLoader(BaseLoader):
    """ Data loader class for JSON documents """

    def __init__(self, string_parsers: List[BaseParser]):
        """
        Initialized the JSON data loader
        :param string_parsers: list of parsers to translate string to Python objects
        """

        self.string_parsers = string_parsers

    def load(self, file_path: str) -> list:
        """
        Loads a specific JSON file of data records into memory
        :param file_path: path to the specific JSON file to load
        :return: list of dictionary records
        """

        with open(file_path) as file:
            records = json.load(file)

        if type(records) != list:
            records = [records]

        # Parse strings into corresponding Python objects
        for record in records:
            for key, val in record.items():
                for parser in self.string_parsers:
                    if parser.check(val):
                        record[key] = parser.parse(val)

        return records
