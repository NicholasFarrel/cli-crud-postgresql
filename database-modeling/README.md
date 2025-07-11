# Database Modeling – Vertical Life

This folder contains the conceptual and relational database design for the **Vertical Life** application, a system designed to register climbing routes, ascents, sectors, and user interactions.

## 📄 Contents

- `database_modeling.pdf`: PDF report describing the conceptual and relational modeling process.
- `database_modeling_source/`: Source files used to generate the LaTeX report.
- `DDL_vertical_life.sql`: SQL script for creating the Vertical Life schema, including tables and constraints.
- `DDL_vertical_life_NO_IDX.sql`: Version of the DDL script without indexes, useful for performance testing comparisons.
- `DML_vertical_life.sql`: SQL script for populating the database with sample data using insert statements.

These files support both the documentation and implementation of the designed schema.

## 🧩 About the Project

The Vertical Life database models a social climbing app, where climbers can:
- Register ascents of climbing routes.
- Follow other climbers or sectors.
- Rate climbs from 1 to 5 stars.
- Track the location and type of routes (Sport, Trad, Boulder).

The model captures complex relationships between climbers, ascents, sectors, and route styles, and was designed to support both functionality and future data analysis.

## 📎 License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.
