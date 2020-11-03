# Data-science: Dialect map server

### About
This repository contains the web server to access the database information.

It will be used in combination with the original PaperScape server, in order to
construct colored areas over the [Dialect map UI][dialect-map-ui] interface,
given the papers categorization over a pair of user specified jargon words frequencies.


### Dependencies
Python dependencies are specified within the `requirements.txt` and `requirements-dev.txt` files.

In order to install the development packages, as long as the defined commit hooks:
```sh
make install-dev
```


### Formatting
All Python files within this project are formatted using [Black][black-web], 
and the custom properties defined in the `pyproject.tml` file. Before each Pull Request:
```sh
make check
```

### Testing
Project testing is performed using [Pytest][pytest-web]. In order to run the tests:
```sh
make test
```


### Docker
In order to build a Docker image out of the project:
```sh
make build
```

In order to run the application as a Docker container:
```sh
docker run --rm -p 8080:8080 dialect-map-server:latest
```


[black-web]: https://black.readthedocs.io/en/stable/
[pytest-web]: https://docs.pytest.org/en/latest/#
[dialect-map-ui]: https://github.com/ds3-nyu-archive/ds-dialect-map-ui
