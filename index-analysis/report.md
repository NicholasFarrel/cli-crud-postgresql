# Report - CRUD and Index Implementation.

## Introduction

This report provides an overview of the implementation for the developed command-line interface (CLI) application, which performs CRUD (Create, Read, Update, Delete) operations on a PostgreSQL database. The application was developed in Python, using the `psycopg2` library for database integration.

In addition to the basic CRUD functions, auxiliary code was implemented to perform a comparative performance analysis of searches with and without the use of indexes, exploring the behavior of `Index Scan` and `Seq Scan` through execution plans (`EXPLAIN ANALYZE`).

To support this analysis, two distinct schemas were created in the database:

- `VerticalLife` — with indexes applied to the columns of interest;
- `VerticalLifeNoIdx` — without indexes, allowing observation of search behavior in an unoptimized scenario.

Throughout this report, the main implementation steps, adaptations made to ensure multi-schema support, and the results obtained from the performance analysis will be described.

---

## 1. Command-Line Application - CRUD `crudVerticalLife.py`

### 1.1. Connection, Schema, Table, and Column Selection Functions

#### `connect_db()`

**Objective:** Establishes a connection to the PostgreSQL database.

**Exception Handling:** In case of a connection error, it displays a message and terminates the program.

#### `choose_schema(cursor)`

**Objective:** Displays a menu with available schemas in the database (excluding internal schemas) and allows the user to choose a schema.

**Exception Handling:** Includes `try/except` to handle invalid user input.

#### `choose_table(cursor, schema)`

**Objective:** Displays a menu with available tables in the specified schema and allows the user to choose a table.

**Exception Handling:** Includes `try/except` to handle invalid user input.

#### `choose_column(cursor, schema_name, table_name)`

**Objective:** Displays a menu with available columns in the specified table and allows the user to choose a column.

**Exception Handling:** Includes `try/except` to handle invalid user input.

### 1.2. Type Conversion Function

#### `get_column_value(cursor, schema_name, table_name, column_name)`

**Objective:** Prompts the user for a filter or insert value for the specified column and returns it correctly converted to the column's type.

**Exception Handling:** Contains a `try/except` block that attempts to convert the user's input to the expected data type of the column. If the conversion fails, an error message is displayed, and the user is prompted to try again.

### 1.3. CRUD Operations

The implementation of CRUD operations focused on security and robustness:

- All database modification operations (Create, Update, Delete) use **parameters** (`%s`) in constructing queries, preventing SQL Injection attacks.
- Transactions are explicitly controlled within modification functions: a `commit` is executed only if the operation is successful; in case of an error, a `rollback` is performed. This ensures that transactions are not left open and that the database maintains its integrity.

```python
# Example of parameter usage in create_record
columns_str = ", ".join(values.keys())
placeholders = ", ".join(["%s"] * len(values))
sql_insert = f"INSERT INTO {schema_name}.{table_name} ({columns_str}) VALUES ({placeholders});"
cursor.execute(sql_insert, tuple(values.values()))

# Example of parameter usage in read_records (with filter)
sql_select = f"""
    SELECT * FROM {schema_name}.{table_name}
    WHERE {filter_column} = %s;
"""
cursor.execute(sql_select, (filter_value,))
````

In these examples, `schema_name`, `table_name`, and `filter_column` are database object names (tables and columns), which are not provided directly by the user but selected from predefined lists or queried from the database schema itself, which already adds a layer of security. The actual values (`values.values()` and `filter_value`) are passed as a tuple to the second argument of `cursor.execute()`. This separation between query definition and the values that populate it prevents SQL Injection attacks. Since user-provided values are not concatenated directly into the query string but passed separately as parameters, the database treats these values as literal data, not as part of the SQL query logic. This blocks attempts to inject malicious code through user inputs.

#### `create_record(conn, cursor, schema_name, table_name)`

**Objective:** Inserts a new record into the specified table. Dynamically queries the table's columns (excluding identity/serial columns) and prompts the user for corresponding values.

#### `read_records(cursor, schema_name, table_name)`

**Objective:** Queries and displays records from the specified table. Optionally allows the user to choose a filter (WHERE condition), with appropriate type conversion.

#### `update_record(conn, cursor, schema_name, table_name)`

**Objective:** Updates one or more records in the specified table. Allows the user to choose the column to update and the new value, as well as the filter column and filter value.

#### `delete_record(conn, cursor, schema_name, table_name)`

**Objective:** Deletes one or more records from the specified table. Allows the user to choose the filter column and filter value.

### 1.4. ASCII Banner

#### `print_ascii_banner()`

**Objective:** Displays an ASCII banner with the name "Vertical Life" in the console, using the `pyfiglet` library. This function is purely aesthetic and serves to add a visual touch when starting the application.

### 1.5. `main()` Function

The `main` function is the central control point of the CRUD application. It allows the user to interactively navigate through three main steps:

  - **Schema selection:** The user selects which database schema they want to operate on (`choose_schema`). The `search_path` is dynamically adjusted to the chosen schema.
  - **Table selection:** The user chooses the table they want to manipulate (`choose_table`).
  - **CRUD operation execution:** An interactive menu allows the execution of CRUD operations on the selected table.

The `main` function uses nested loops to allow fluid navigation:

  - The outer loop allows changing schemas at any time.
  - The intermediate loop allows changing tables within the schema.
  - The inner loop controls the CRUD menu for the chosen table.

This structure makes the application flexible and adaptable to a multi-schema and multi-table scenario.

-----

## 2\. Index and Search Implementation

### 2.1. Performance Analysis with Indexes

To evaluate the impact of indexes on query performance, two distinct schemas were created in the database: one with an index (`VerticalLife`) and one without an index (`VerticalLifeNoIdx`) on the climber's name column. To simulate a high-volume data environment and make performance tests more realistic, 100,000 name entries were generated for each schema. This data population was performed using the Python script `name_generator.py`, which automates the creation of random names and their insertion into the database.

The tests were executed using the `teste_busca_indices.py` script, which employs the `EXPLAIN ANALYZE` command to measure execution time and analyze the query plan in both schemas. For each schema, searches were performed in two distinct cases:

  - **Easiest name to find:** The first climber in the table, i.e., the record with the smallest `IDEscalador`. This record is considered easy to find in a database without an index because a Sequential Scan traverses the table in physical order, and the first record is found early in the scan.

  - **Hardest name to find:** The last climber in the table, i.e., the record with the largest `IDEscalador`. This record is considered difficult to find without an index because, in a Sequential Scan, the DBMS needs to traverse the entire table until the end to locate the record, resulting in an execution time proportional to the table size.

With the use of an index (Index Scan), the physical position of the record no longer impacts search time, making access equally fast for any name, regardless of its position in the table.

```
1 - Test search by first name (VerticalLife)------------------------------------------

== EXPLAIN ANALYZE for name 'Calango' in VerticalLife schema ==
Index Scan using idx_escalador_nomeescalador on escalador  (cost=0.42..8.44 rows=1 width=18) (actual time=0.037..0.037 rows=1 loops=1)
  Index Cond: ((nomeescalador)::text = 'Calango'::text)

Planning Time: 0.053 ms
Execution Time: 0.046 ms

2 - Test search by last name (VerticalLife)--------------------------------------------

== EXPLAIN ANALYZE for name 'James Bruyere' in VerticalLife schema ==
Index Scan using idx_escalador_nomeescalador on escalador  (cost=0.42..8.44 rows=1 width=18) (actual time=0.035..0.036 rows=1 loops=1)
  Index Cond: ((nomeescalador)::text = 'James Bruyere'::text)

Planning Time: 0.045 ms
Execution Time: 0.044 ms

3 - Test search by first name (VerticalLifeNoIdx)-------------------------------------

== EXPLAIN ANALYZE for name 'Calango' in VerticalLifeNoIdx schema ==
Seq Scan on escalador  (cost=0.00..1867.06 rows=1 width=18) (actual time=0.005..4.640 rows=1 loops=1)
  Filter: ((nomeescalador)::text = 'Calango'::text)
  Rows Removed by Filter: 100004

Planning Time: 0.029 ms
Execution Time: 4.649 ms

4 - Test search by last name (VerticalLifeNoIdx)----------------------------------------

== EXPLAIN ANALYZE for name 'James Clark' in VerticalLifeNoIdx schema ==
Seq Scan on escalador  (cost=0.00..1867.06 rows=1 width=18) (actual time=0.954..5.257 rows=4 loops=1)
  Filter: ((nomeescalador)::text = 'James Clark'::text)
  Rows Removed by Filter: 100001

Planning Time: 0.038 ms
Execution Time: 5.265 ms
```

### 2.2. Results Analysis

The results confirm the effectiveness of indexes in optimizing searches. In the `VerticalLife` schema (with an index), both the search for the first and last names showed extremely low execution times (in milliseconds), and the execution plan shows an `Index Scan`. This demonstrates that the index allowed the DBMS to locate records directly, without the need to scan the entire table.

On the other hand, in the `VerticalLifeNoIdx` schema (without an index), searches resulted in a `Seq Scan` (sequential table scan). Although the search for the first name was relatively fast, the search for the last name took significantly longer. This is because the DBMS had to traverse the entire table to find the desired record, which is inefficient for large volumes of data. The time difference between searches with and without an index is clear, demonstrating the performance gain provided by indexing.
