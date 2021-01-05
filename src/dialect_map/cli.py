#!/usr/bin/env python

import click
from dialect_map_data import FILES_MAPPINGS

from .storage import JSONFileLoader
from .storage import SQLAlchemyDatabase


@click.group()
def main():
    pass


@main.command()
@click.option(
    "--url",
    envvar="DIALECT_MAP_DB_URL",
    default="postgresql+psycopg2://dm:dmpwd@localhost/dialect_map",
    type=str,
)
def load_db(url: str):
    """
    Loads testing data into the specified database instance
    :param url: connection URL for the database to setup
    """

    try:
        loader = JSONFileLoader()
        database = SQLAlchemyDatabase(url, files_loader=loader)
        database.setup()
    except Exception as e:
        print(e)
        return

    for mapping in FILES_MAPPINGS:
        database.load(
            file_path=mapping.file,
            data_model=mapping.model,
        )


@main.command()
@click.option(
    "--url",
    envvar="DIALECT_MAP_DB_URL",
    default="postgresql+psycopg2://dm:dmpwd@localhost/dialect_map",
    type=str,
)
def setup_db(url: str):
    """
    Creates all the database schema tables that do not exist
    :param url: connection URL for the database to setup
    """

    try:
        database = SQLAlchemyDatabase(url)
        database.setup()
    except Exception as e:
        print(e)


@main.command()
@click.option(
    "--url",
    envvar="DIALECT_MAP_DB_URL",
    default="postgresql+psycopg2://dm:dmpwd@localhost/dialect_map",
    type=str,
)
@click.option(
    "--force",
    is_flag=True,
    default=False,
    type=bool,
)
def teardown_db(url: str, force: bool):
    """
    Destroys all the empty database schema tables, unless --force is used
    :param url: connection URL for the database to tear down
    :param force: whether to delete non-empty tables
    """

    check = not force

    try:
        database = SQLAlchemyDatabase(url)
        database.teardown(check=check)
    except Exception as e:
        print(e)
