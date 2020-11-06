#!/usr/bin/env python

import click
from config import ApplicationConfig
from config import EnvironmentConfigLoader
from storage import SQLAlchemyDatabase


@click.group()
def main():
    pass


@main.command()
def setup_db():
    """ Creates all the database schema tables that do not exist """

    loader = EnvironmentConfigLoader()
    config = ApplicationConfig(loader)

    database = SQLAlchemyDatabase(config.database_url)
    database.setup()


@main.command()
@click.option("--force", is_flag=True, default=False)
def teardown_db(force: bool):
    """ Destroys all the empty database schema tables, unless --force is used """

    check = not force
    loader = EnvironmentConfigLoader()
    config = ApplicationConfig(loader)

    database = SQLAlchemyDatabase(config.database_url)
    database.teardown(check=check)


if __name__ == "__main__":
    main()
