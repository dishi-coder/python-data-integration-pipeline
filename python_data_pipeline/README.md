# Python Data Integration and Transformation Pipeline

A beginner-friendly data engineering project that demonstrates how to fetch JSON data from a REST API, clean and transform it with Python, and load it into CSV and SQLite.

## What it does

1. Extracts user records from the JSONPlaceholder REST API.
2. Selects useful fields from nested JSON data.
3. Trims text, handles missing values, and removes duplicate email records.
4. Saves the cleaned data to a CSV file.
5. Loads the same data into a SQLite database.
6. Runs an SQL query to count users by city.

## Tech stack

- Python
- REST API, HTTP GET, JSON
- pandas
- SQLite and SQL
- CSV
- Git / GitHub (for version control)

## Requirements

- Python 3.10 or newer
- Internet connection for the API request

## Run in VS Code

Open this project folder in VS Code. In the terminal, run:

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python main.py
```

If `py` does not work, try `python` instead.

## Output

After a successful run, the `output` folder will contain:

- `cleaned_users.csv` — cleaned records in CSV format
- `pipeline.db` — SQLite database containing the `users` table

The program also prints a small SQL summary showing the number of users per city.

## Data source

JSONPlaceholder users endpoint: https://jsonplaceholder.typicode.com/users

This is a public demo API. The project uses sample user data for learning; it is not intended for production use.

## Possible improvements

- Add logging and automated tests.
- Schedule the pipeline to run regularly.
- Add validation rules and data-quality reports.
- Connect to a cloud data warehouse such as BigQuery after learning the basics.
