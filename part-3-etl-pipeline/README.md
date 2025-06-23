## Problem - Part 3: ETL Pipeline

- Provide a tool/script that extracts data from the provided JSON file, transforms the data by applying some cleaning or aggregation, and loads it into the database.
- Explain how you would schedule and monitor this pipeline using tools like Apache Airflow.

## Solution

My approach to this part was to iterate and build functionality in an agile way:

1. Understand the `SpaceX API` and its `data model`.
2. Design a simple `SQL schema` following a `Star schema data modeling strategy`.
3. Develop `Python APIs` to `extract, transform, and load` the data entities.
4. Create a simple `Python ETL script` to demonstrate the end-to-end use case.
5. Implement an `Apache Airflow solution` to orchestrate the Python DAG.

This `Part 3` is organized into the following sections:

- [ETL API and SQL](etl/README.md).
- [Simple Pyton ETL solution](without-airflow/README.md)
- [Apache Airflow ETL solution](with-airflow/README.md)
