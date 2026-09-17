# Python Data Toolkit

A small Python data-processing and cleaning toolkit built with intermediate Python concepts. The project loads a messy CSV dataset, cleans and validates the records, handles duplicate IDs, performs basic analysis, and generates a summary report.

The project uses only the **Python standard library**.

## Features

* Reads data from a CSV file
* Cleans and validates records
* Converts written ages into numeric values
* Handles missing and invalid data
* Detects exact and conflicting duplicate IDs
* Uses generators for processing cleaned records
* Provides basic dataset statistics
* Uses a decorator to measure execution time
* Generates a text summary report
* Organizes functionality across separate Python modules

## Project Structure

```text
.
├── clean_age.py
├── data and summary/
│   ├── messy_people.csv
│   └── report-summary.txt
├── dataset.py
├── main.py
├── record.py
└── utils.py
```

### Modules

* **`main.py`** — Entry point for running the toolkit.
* **`dataset.py`** — Handles dataset loading, cleaning, duplicate handling, analysis, and report generation.
* **`record.py`** — Defines the `Record` dataclass and record validation.
* **`clean_age.py`** — Handles conversion and validation of age values.
* **`utils.py`** — Contains reusable utilities such as the execution-time decorator.
* **`data and summary/`** — Contains the source CSV dataset and generated summary report.

## Running the Project

Make sure Python is installed, then run:

```bash
python main.py
```

No third-party packages are required.

## Output

The program prints a dataset summary containing information such as:

* Rows loaded and dropped
* Reasons rows were dropped
* Average score
* Oldest and youngest person
* Number of people per city
* Final number of cleaned records

A summary is also generated and written to:

```text
data and summary/report-summary.txt
```
