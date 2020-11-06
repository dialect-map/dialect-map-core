# -*- coding: utf-8 -*-

import os
from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Union


class ConfigLoader(metaclass=ABCMeta):
    """ Interface for configuration loader classes """

    @abstractmethod
    def load_argument(self, data_type: type, name: str, default: Any) -> Any:
        """
        Loads a single argument from an external configuration source
        :param data_type: type to cast the value to
        :param name: name serving as key in the external source
        :param default: default value in case the key is not found
        :return: parsed value
        """

        raise NotImplementedError()

    @abstractmethod
    def load_arguments(self, arguments: dict) -> dict:
        """
        Loads multiple arguments from an external configuration source
        :param arguments: dictionary of tuple defined arguments
        :return: dictionary of parsed values
        """

        raise NotImplementedError()


class EnvironmentConfigLoader(ConfigLoader):
    """ Configuration loader using the OS environment variables """

    @staticmethod
    def _parse_value(data_type: type, name: str, default: Any) -> Any:
        """
        Parses a single argument from the list of OS env. variables
        :param data_type: type to cast the value to
        :param name: name serving as key in the environment
        :param default: default value in case the key is not found
        :return: parsed value
        """

        value = os.getenv(name, default)
        value = data_type(value)
        return value

    def load_argument(self, data_type: type, name: str, default: Any) -> Any:
        """
        Loads a single argument from the OS env.
        :param data_type: type to cast the value to
        :param name: name serving as key in the environment
        :param default: default value in case the key is not found
        :return: parsed value
        """

        return self._parse_value(data_type, name, default)

    def load_arguments(self, args: Union[dict, tuple]) -> dict:
        """
        Recursive function to load multiple arguments from the OS env.
        :param args: structure of defined arguments
        :return: dictionary of parsed values
        """

        if isinstance(args, dict):
            return {k: self.load_arguments(v) for k, v in args.items()}

        if isinstance(args, tuple):
            return self._parse_value(*args)

        raise ValueError("Invalid builder argument")
