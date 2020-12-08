# Dialect map core

### About
This repository contains the web server to access the database information.

It will be used in combination with the original PaperScape server, in order to
construct colored areas over the [Dialect map UI][dialect-map-ui] interface,
given the papers categorization over a pair of user specified jargon words frequencies.


### Dependencies
Python dependencies are specified within the `setup.py` file.

In order to install the development packages, as long as the defined commit hooks:
```sh
pip install ".[dev]"
pre-commit install
```


### Formatting
All Python files are formatted using [Black][black-web],  and the custom properties defined
in the `pyproject.toml` file.
```sh
make check
```

### Testing
Project testing is performed using [Pytest][pytest-web]. In order to run the tests:
```sh
make test
```


[black-web]: https://black.readthedocs.io/en/stable/
[pytest-web]: https://docs.pytest.org/en/latest/#
[dialect-map-ui]: https://github.com/ds3-nyu-archive/ds-dialect-map-ui
