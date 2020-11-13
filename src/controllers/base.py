# -*- coding: utf-8 -*-

from abc import ABCMeta
from abc import abstractmethod
from models import Base


class BaseController(metaclass=ABCMeta):
    """ Interface for the data controllers """

    @abstractmethod
    def get(self, id: str) -> Base:
        """
        Gets a database record by its ID
        :param id: ID of the database entry
        :return: data object representing the database record
        """

        raise NotImplementedError()

    @abstractmethod
    def create(self, data_object: Base) -> str:
        """
        Creates a new database record given its object properties
        :param data_object: object properties to create the record with
        :return: ID of the created record
        """

        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: str) -> str:
        """
        Deletes a database record by its ID
        :param id: ID of the database entry
        :return: ID of the deleted record
        """

        raise NotImplementedError()
