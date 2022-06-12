# -*- coding: utf-8 -*-

import pytest

from click.testing import CliRunner

from src.dialect_map_core.cli import main


@pytest.fixture(scope="module")
def env() -> dict:
    """
    Defines the set of environment variables available to the CLI runner
    :return: dict of environment variables
    """

    return {
        "DIALECT_MAP_DB_URL": "sqlite:///:memory:",
    }


def test_cli_load_db(env: dict):
    """
    Tests the invocation of the DB loading CLI command
    :param env: dictionary of environment variables
    """

    runner = CliRunner(env=env)
    result = runner.invoke(main, "load-db")

    assert result.exit_code == 0
    assert result.output == ""


def test_cli_setup_db(env: dict):
    """
    Tests the invocation of the DB set-up CLI command
    :param env: dictionary of environment variables
    """

    runner = CliRunner(env=env)
    result = runner.invoke(main, "setup-db")

    assert result.exit_code == 0
    assert result.output == ""


def test_cli_teardown_db(env: dict):
    """
    Tests the invocation of the DB tear-down CLI command
    :param env: dictionary of environment variables
    """

    runner = CliRunner(env=env)
    result = runner.invoke(main, "teardown-db")

    assert result.exit_code == 0
    assert result.output == ""

    result = runner.invoke(main, "teardown-db --force")

    assert result.exit_code == 1
    assert result.output != ""
