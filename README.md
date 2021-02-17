# Dialect map core

### About
This repository contains core models and controllers for the database.

It is used as a dependency package on the HTTP API components that manage
public and private access to the database information. The public API is used by the
[Dialect map UI][dialect-map-ui], while the private one by a set of data-ingestion jobs
which populate the database.


### Documentation
For more information about the interaction with this repository:
- [Database setup][docs-database].
- [Models definitions][docs-models].


### Dependencies
Python dependencies are specified within the `setup.py` file.

In order to install the development packages, as long as the defined commit hooks:
```sh
pip install ".[dev]"
pre-commit install
```


### Formatting
All Python files are formatted using [Black][black-web], and the custom properties defined
in the `pyproject.toml` file.
```sh
make check
```


### Testing
Project testing is performed using [Pytest][pytest-web]. In order to run the tests:
```sh
make test
```


### Tagging
Commits can be tagged to create _informal_ releases of the package. In order to do so:

1. Bump up the package version (`VERSION`) following [Semantic Versioning][semantic-web].
2. Create and push a tag: `make tag`.


[dialect-map-ui]: https://github.com/dialect-map/dialect-map-ui
[docs-database]: docs/database.md
[docs-models]: docs/models.md
[black-web]: https://black.readthedocs.io/en/stable/
[pytest-web]: https://docs.pytest.org/en/latest/#
[semantic-web]: https://semver.org/
