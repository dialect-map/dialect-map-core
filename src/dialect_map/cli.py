#!/usr/bin/env python

import sys
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
    help="Connection URL for the database to load",
    type=str,
)
def load_db(url: str):
    """Loads testing data into the specified database instance"""

    try:
        loader = JSONFileLoader()
        database = SQLAlchemyDatabase(url, file_loader=loader)
        database.setup()
    except Exception as e:
        click.echo(e, err=True)
        sys.exit(1)

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
    help="Connection URL for the database to setup",
    type=str,
)
def setup_db(url: str):
    """Creates all the database tables that do not exist"""

    try:
        database = SQLAlchemyDatabase(url)
        database.setup()
    except Exception as e:
        click.echo(e, err=True)
        sys.exit(1)


@main.command()
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

    try:
        database = SQLAlchemyDatabase(url)
        database.teardown(check=check)
    except Exception as e:
        click.echo(e, err=True)
        sys.exit(1)
