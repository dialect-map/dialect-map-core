# -*- coding: utf-8 -*-

from .loaders import ConfigLoader


class ApplicationConfig:
    """ Application global configuration """

    def __init__(self, loader: ConfigLoader):
        """
        Loads the application configuration from an external source
        :param loader: external source configuration loader
        """

        self.database_url = loader.load_argument(
            name="DIALECT_MAP_DB_URL",
            default="postgresql+psycopg2://dm:dmpwd@localhost/dialect_map",
            data_type=str,
        )

        self.log_level = loader.load_argument(
            name="DIALECT_MAP_LOG_LEVEL",
            default="INFO",
            data_type=str,
        )
