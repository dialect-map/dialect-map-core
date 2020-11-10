# Development

## Configuration
The configuration of the server is controlled by the following environment variables:

- **DIALECT_MAP_DB_URL**: SQLAlchemy database URL for the database connection.
- **DIALECT_MAP_LOG_LEVEL**: Logging level. Check available levels [here][python-logging-levels].


## Setup
To set up the necessary resources for a server instance to work:

#### 1. Install dependencies
```sh
$ pip install -r requirements.txt
```

#### 2. Start a local PostgreSQL database instance
```sh
$ postgres -D /usr/local/var/postgres
```

#### 3. Create admin user and database
```sh
$ psql --dbname=postgres
postgres=# CREATE USER dm;
postgres=# ALTER USER dm WITH PASSWORD 'dmpwd';
postgres=# CREATE DATABASE dialect_map WITH OWNER dm;
```

#### 4. Create the database tables
```sh
$ python3 src/commands.py setup-db
```


## Run
To start a local development server:

#### 1. Set necessary env. variables
```sh
$ export DIALECT_MAP_DB_URL=postgresql+psycopg2://dm:dmpwd@localhost/dialect_map
```

#### 2. Run the server
```sh
$ ./scripts/start_flask.sh
```


[python-logging-levels]: https://docs.python.org/3.6/library/logging.html#levels
