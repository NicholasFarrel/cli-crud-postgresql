# CLI - PostgreSQL Interactive CRUD Tool

This module offers a flexible command-line interface (CLI) to interact with **any user-defined PostgreSQL database**, allowing you to perform CRUD operations without hardcoding SQL queries. It is not tied to a specific schema and is compatible with any database created by the user (excluding PostgreSQL's default system databases like `postgres`, `template1`, etc.).

## Features

- 🔄 Supports Create, Read, Update, and Delete operations
- 🧠 Introspects the schema to dynamically adapt to any table
- 👨‍💻 Designed for rapid prototyping, learning, and testing in PostgreSQL environments
- 📄 Automatically lists available tables and columns
- 🛠️ Includes a `name_generator.py` utility to generate test names

## Files

- `crudVerticalLife.py`: Core CLI tool for interacting with PostgreSQL databases.
- `name_generator.py`: Utility for generating random name data (used for inserts or testing).
- `report.md`: Documentation explaining the purpose, logic, and design choices behind the CLI tool.

## Requirements

- Python 3.x  
- [`psycopg2`](https://pypi.org/project/psycopg2/)  
- A user-created PostgreSQL database with accessible credentials

## How to Use

1. Ensure your PostgreSQL server is running.
2. Open the script `crudVerticalLife.py` and adjust the connection string:
   ```python
   conn = psycopg2.connect(
       dbname="your_db_name",
       user="your_username",
       password="your_password",
       host="localhost",
       port="5432"
   )
   ```
3. Run the CLI:
   ```bash
   python crudVerticalLife.py
   ```

Follow the prompts to select tables and perform operations.

## When to Use

- Educational purposes (e.g., practicing SQL logic)
- Interacting with freshly designed schemas
- Verifying CRUD logic during schema development
- Replacing manually written SQL during early prototyping
