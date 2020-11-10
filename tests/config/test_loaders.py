# -*- coding: utf-8 -*-

import os
import pytest
from config import EnvironmentConfigLoader


@pytest.fixture(scope="module")
def env_loader():
    """ Generates a EnvironmentConfigLoader object """

    return EnvironmentConfigLoader()


@pytest.fixture(scope="module")
def config_args():
    """ Generates a list of configurable arguments """

    return {
        "nested_args": {
            "test_float": (float, "TEST_FLOAT_ENV_VALUE", 1.5),
            "test_integer": (int, "TEST_INTEGER_ENV_VALUE", 1),
            "test_string": (str, "TEST_STRING_ENV_VALUE", "default"),
        },
    }


def test_env_loader_parsing(env_loader: EnvironmentConfigLoader, config_args: dict):
    """
    Tests the correct env. vars parsing of the EnvironmentConfigLoader
    :param env_loader: loader to test
    :param config_args: dict of configurable arguments
    """

    os.environ["TEST_FLOAT_ENV_VALUE"] = "2.5"
    os.environ["TEST_INTEGER_ENV_VALUE"] = "2"

    parsed = env_loader.load_arguments(config_args)
    parsed = parsed["nested_args"]

    assert parsed["test_float"] == 2.5
    assert parsed["test_integer"] == 2
    assert parsed["test_string"] == "default"

    del os.environ["TEST_FLOAT_ENV_VALUE"]
    del os.environ["TEST_INTEGER_ENV_VALUE"]
