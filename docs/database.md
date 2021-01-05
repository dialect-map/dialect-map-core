# Database operations


## Introduction
The `dialect_map` package defines a CLI tool called `dm-admin` that can be used to perform
setup, teardown and loading operations on the desired SQL database.

The `dialect_map_data` package contains testing data files that can be loaded into any database
thanks to the mapping between these files and their corresponding data model classes.

For now, the only supported SQL database is _PostgreSQL_, although future ones can be easily added
given the flexibility of the library used ([SQLAlchemy][sqlalchemy-website]).


## Database
To start a local PostgreSQL database, install the PostgreSQL binaries through their website or by one
of your OS package managers (i.e. `apt` for Ubuntu, `brew` for macOS...).

Then run:
```sh
$ postgres -D /usr/local/var/postgres
```

Finally, create the admin user and database partition by running:
```sh
$ psql --dbname=postgres
postgres=# CREATE USER dm;
postgres=# ALTER USER dm WITH PASSWORD 'dmpwd';
postgres=# CREATE DATABASE dialect_map WITH OWNER dm;
```


## CLI Commands
List of available operations to perform using the _Dialect Map_ CLI:

#### Setup
Creates all the necessary tables, indexes, relationships and constraints.
```sh
$ dm-admin setup-db
```

| PARAMETER   | ENV. VARIABLE         | REQUIRED | DEFAULT | DESCRIPTION                        |
|-------------|-----------------------|----------|---------|------------------------------------|
| --url       | DIALECT_MAP_DB_URL    | No       | ...     | Database connection URL            |

#### Teardown
Deletes all the tables, indexes, relationships and constraints.
```sh
$ dm-admin teardown-db
```

| PARAMETER   | ENV. VARIABLE         | REQUIRED | DEFAULT | DESCRIPTION                        |
|-------------|-----------------------|----------|---------|------------------------------------|
| --url       | DIALECT_MAP_DB_URL    | No       | ...     | Database connection URL            |
| --force     | -                     | No       | False   | Whether to delete non-empty tables |

#### Load
Loads testing data into the desired database instance
```sh
$ dm-admin load-db
```

| PARAMETER   | ENV. VARIABLE         | REQUIRED | DEFAULT | DESCRIPTION                        |
|-------------|-----------------------|----------|---------|------------------------------------|
| --url       | DIALECT_MAP_DB_URL    | No       | ...     | Database connection URL            |


[sqlalchemy-website]: https://www.sqlalchemy.org/
