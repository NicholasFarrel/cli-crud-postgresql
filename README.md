# CLI CRUD System for PostgreSQL — VerticalLife Project

This project provides a robust command-line interface (CLI) for performing CRUD (Create, Read, Update, Delete) operations on a PostgreSQL database, with support for multiple schemas and tables. The system is designed to be secure, modular, and user-friendly, enabling dynamic interaction with database structure.

Additionally, the repository includes performance testing scripts to compare search efficiency with and without indexes, highlighting the impact of index optimization in PostgreSQL.

---

## 📁 Repository Structure

| File                          | Description                                                        |
|-------------------------------|--------------------------------------------------------------------|
| `crudVerticalLife.py`        | Main CLI application for performing CRUD operations                |
| `name_generator.py`          | Script to populate the database with random names                  |
| `teste_busca_indices.py`     | Performance testing with `EXPLAIN ANALYZE`                         |
| `DDL_vertical_life.sql`      | Schema and index creation (with index)                             |
| `DDL_vertical_life_NO_IDX.sql` | Schema creation without indexes                                    |
| `DML_vertical_life.sql`      | Sample data insertion statements                                   |
| `relationalVerticalLife.png` | ER diagram of the database schema                                  |
| `README.md`                  | Project description and usage instructions                         |

---

## 🔧 Features

- Interactive CLI for CRUD operations with schema/table/column selection  
- Automatic data type handling and validation  
- Support for multiple PostgreSQL schemas (`VerticalLife` and `VerticalLifeNoIdx`)  
- Secure query execution using parameterized statements (protection against SQL injection)  
- Controlled transaction management (commit/rollback)  
- Performance comparison of indexed vs non-indexed search using `EXPLAIN ANALYZE`

---

## 🚀 Getting Started

1. Ensure you have PostgreSQL installed and running.
2. Create the database and load the schemas using the provided `.sql` files.
3. (Optional) Populate the database using `name_generator.py`.
4. Run the CRUD interface:

```bash
python crudVerticalLife.py
