#!/usr/bin/env python

import functools
import sys

from typing import Any
from typing import Callable

import click

from dialect_map_data import FILES_MAPPINGS

from .storage import BaseDatabaseError
from .storage import JSONFileLoader
from .storage import SQLDatabase
from .storage import get_error_message


def click_command_wrapped(func: Callable) -> Callable:
    """
    Decorator to simplify error handling across CLI commands
    :param func: CLI command function to wrap
    :return: CLI command function wrapped
    """

    @functools.wraps(func)
    def func_wrapper(*args, **kwargs) -> Any:

        try:
            func(*args, **kwargs)
        except BaseDatabaseError as e:
            click.echo(get_error_message(e), err=True)
            sys.exit(1)
        except Exception as e:
            click.echo(e, err=True)
            sys.exit(1)

    return func_wrapper


@click.group()
def main():
    pass


@main.command()
@click_command_wrapped
@click.option(
    "--url",
    envvar="DIALECT_MAP_DB_URL",
    default="postgresql+psycopg2://dm:dmpwd@localhost/dialect_map",
    help="Connection URL for the database to load",
    type=str,
)
def load_db(url: str):
    """Loads testing data into the specified database instance"""

    loader = JSONFileLoader()
    database = SQLDatabase(url, file_loader=loader)
    database.setup()

    for mapping in FILES_MAPPINGS:
        database.load(
            file_path=mapping.file,
            data_model=mapping.model,
        )


@main.command()
@click_command_wrapped
@click.option(
    "--url",
    envvar="DIALECT_MAP_DB_URL",
    default="postgresql+psycopg2://dm:dmpwd@localhost/dialect_map",
    help="Connection URL for the database to setup",
    type=str,
)
def setup_db(url: str):
    """Creates all the database tables that do not exist"""

    database = SQLDatabase(url)
    database.setup()


@main.command()
@click_command_wrapped
@click.option(
    "--url",
    envvar="DIALECT_MAP_DB_URL",
    default="postgresql+psycopg2://dm:dmpwd@localhost/dialect_map",
    help="Connection URL for the database to tear down",
    type=str,
)
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Whether to delete non-empty tables",
    type=bool,
)
def teardown_db(url: str, force: bool):
    """Destroys all the empty database tables"""

    check = not force

    database = SQLDatabase(url)
    database.teardown(check=check)
