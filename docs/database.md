# Database operations


## Introduction
The database related contents are split between two packages:

- `dialect_map`: defining a CLI (`dm-admin`) to perform setup, teardown and loading operations.
- `dialect_map_data`: containing testing files loadable thanks to the _file-to-model_ mappings.

For now, the only supported SQL database is _PostgreSQL_, although other ones can be easily added
thanks to the use of ([SQLAlchemy][sqlalchemy-website]).


## Database
To start a local PostgreSQL database, install the PostgreSQL binaries through their website or
by one of your OS package managers

- For Ubuntu: `apt install postgresql`.
- For Mac OS: `brew install postgresql`.

Then run:
```sh
$ sudo mkdir -p /usr/local/var/postgres
$ sudo chown $(whoami) /usr/local/var/postgres
$ initdb -D /usr/local/var/postgres
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
