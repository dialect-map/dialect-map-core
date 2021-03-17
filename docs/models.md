# Data models


## Introduction
The `dialect_map` package defines a series of data models that are later on used to create
their corresponding database tables. These models follow classic SQL properties, constraints
and syntax, although their usage has only been tested on _PostgreSQL_ databases.


## Types
All data models inherit a set of properties from one of the base model types:
- **Static:** those that cannot be updated over time.
- **Archival:** those that cannot be updated over time, only archived.
- **Evolving:** those that can be updated over time.

The expression _"can be updated over time"_ does **not** refer to the use of SQL `UPDATE` operations to
modify the information of a given record, but to the insertion of multiple records with: the same ID,
updated information, and successive and incremental _revision_ values.


## Common properties
Depending on the type of data model, there is a subset of Python properties available to use:

### Static models:
- `id`: the unique identifier of the data record.
- `data`: the set of key-value pairs with the record data.

### Archival models:
- `id`: the unique identifier of the data record.
- `data`: the set of key-value pairs with the record data.
- `archived`: whether the data record has been archived.

### Evolving models:
- `id`: the unique identifier of the data record.
- `rev`: the unique revision of the data record.
- `data`: the set of key-value pairs with the record data.


## Common fields
Depending on the type of data model, there is a subset of data fields available to query:

### Static models:
- `created_at`: UTC timestamp when the object referenced with the used ID was created.
- `audited_at`: UTC timestamp when the database record was stored.

### Archival models:
- `created_at`: UTC timestamp when the object referenced with the used ID was created.
- `archived_at`: UTC timestamp when the object referenced with the used ID was archived.
- `audited_at`: UTC timestamp when the database record was stored.

### Evolving models:
- `created_at`: UTC timestamp when the object referenced with the used ID was created.
- `updated_at`: UTC timestamp when the object referenced with the used ID was updated.
- `audited_at`: UTC timestamp when the database record was stored.

### Explanation
There exist a clear differentiation across the set of common fields inherit from the base models.

On one hand, `created_at` and `updated_at` target the object being referenced by the record ID.
Although the object would sometimes be a made up one created by us (i.e. a _metrics_ record),
some others it would be an external object to our system (i.e. an _arxiv_ paper).
For this reason, these fields must contain the **values coming from the referenced object**
when possible, and only default to the current timestamp when that information is not available.

On the other hand, `archived_at` and `audited_at` are _control_ fields, defined only for debugging purposes.
These field **must not** be inserted by the user, as it is automatically filled by the back-end.
