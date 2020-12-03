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


### Docker
There is a `Makefile` to perform both Docker `build` and `push` operations.

The project is currently designed to be deployed in the _DS3-Dialect-Map_ GCP project,
so the initial step involves using [gcloud][gcloud-cli-setup] CLI tool to log in with GCP:

```sh
gcloud login
gcloud auth configure-docker
```

In order to build a Docker image out of the project:
```sh
make build
```

To push the image to the GCP registry:
```sh
export GCP_PROJECT="ds3-dialect-map"
export GCP_REGISTRY="us.gcr.io"
make push
```


### Deployment
This project uses a set of env. variables to configure certain aspects of the API:

| ENV VARIABLE             | DEFAULT            | REQUIRED | DESCRIPTION                                   |
|--------------------------|--------------------|----------|-----------------------------------------------|
| DIALECT_MAP_DB_URL       | ...                | No       | Database connection URL                       |
| DIALECT_MAP_LOG_LEVEL    | INFO               | No       | Log messages level                            |


[black-web]: https://black.readthedocs.io/en/stable/
[pytest-web]: https://docs.pytest.org/en/latest/#
[dialect-map-ui]: https://github.com/ds3-nyu-archive/ds-dialect-map-ui
[gcloud-cli-setup]: https://cloud.google.com/sdk/docs/install
