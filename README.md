# CLI CRUD PostgreSQL – Vertical Life

This repository contains the development of a PostgreSQL-based CLI system designed for a rock climbing application named **Vertical Life**. The project covers three main stages: data modeling, command-line interaction, and index performance analysis.

## 📁 Structure

- **`database-modeling/`**  
  Contains the **conceptual and relational database design** for the Vertical Life system, including ER diagrams, DDL/DML SQL scripts, and the LaTeX report describing entities and relationships.

- **`cli/`**  
  A **command-line interface** in Python that provides general PostgreSQL CRUD operations. Though tested on the Vertical Life schema, this CLI is fully reusable and adaptable to any PostgreSQL schema.

- **`index-analysis/`**  
  Scripts and resources for **analyzing performance of SQL indexes** using synthetic data generation and query benchmarking. Useful for understanding the impact of indexing strategies on SELECT and JOIN operations.

## 🛠 Technologies Used

- PostgreSQL (SQL)
- Python 3
  - `psycopg2` for database connection
  - `argparse` and `os` for CLI utilities
  - `time`, `random`, `faker` for benchmarks and data generation
- LaTeX for database modeling report
- Markdown for documentation

## ⚙️ Setup

1. Ensure you have a running PostgreSQL server.
2. Use the SQL scripts in `database-modeling/` to create the schema and populate data.
3. Run CLI operations using scripts inside the `cli/` folder.
4. Use `index-analysis/` to explore query performance with and without indexes.

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.
