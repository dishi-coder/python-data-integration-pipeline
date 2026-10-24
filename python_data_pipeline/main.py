"""
Python Data Integration and Transformation Pipeline
Fetches JSON data from a REST API, cleans/transforms it,
then saves the result to CSV and SQLite.
"""

import sqlite3
from pathlib import Path

import pandas as pd
import requests

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

API_URL = "https://jsonplaceholder.typicode.com/users"
CSV_PATH = OUTPUT_DIR / "cleaned_users.csv"
DB_PATH = OUTPUT_DIR / "pipeline.db"


def fetch_data():
    """Fetch JSON records from a REST API."""
    print("Fetching data from REST API...")
    response = requests.get(API_URL, timeout=15)
    response.raise_for_status()
    data = response.json()

    if not isinstance(data, list):
        raise ValueError("Expected the API to return a list of records.")

    print(f"Fetched {len(data)} records.")
    return data


def transform_data(records):
    """Select useful fields, handle missing values, and remove duplicates."""
    rows = []

    for record in records:
        address = record.get("address") or {}
        company = record.get("company") or {}

        rows.append({
            "user_id": record.get("id"),
            "name": record.get("name"),
            "email": record.get("email"),
            "city": address.get("city"),
            "company": company.get("name"),
        })

    df = pd.DataFrame(rows)

    # Standardize text fields and convert empty strings to missing values.
    for column in ["name", "email", "city", "company"]:
        df[column] = df[column].astype("string").str.strip()
        df[column] = df[column].replace("", pd.NA)

    before = len(df)

    # Remove duplicate records using email as the identifying field.
    df = df.drop_duplicates(subset=["email"], keep="first")

    # Keep records that have the essential fields needed for this dataset.
    df = df.dropna(subset=["user_id", "name", "email"])

    # Fill optional missing values so the output is easier to analyse.
    df["city"] = df["city"].fillna("Unknown")
    df["company"] = df["company"].fillna("Unknown")

    df["user_id"] = df["user_id"].astype(int)
    df = df.sort_values("user_id").reset_index(drop=True)

    print(f"Transformation complete: {before - len(df)} duplicate/incomplete rows removed.")
    print(f"Clean records: {len(df)}")
    return df


def save_to_csv(df):
    """Save transformed data as CSV."""
    df.to_csv(CSV_PATH, index=False)
    print(f"CSV saved to: {CSV_PATH}")


def save_to_sqlite(df):
    """Load transformed data into a SQLite database table."""
    with sqlite3.connect(DB_PATH) as connection:
        df.to_sql("users", connection, if_exists="replace", index=False)

        # Example SQL analysis: number of users per city.
        summary = pd.read_sql_query(
            """
            SELECT city, COUNT(*) AS user_count
            FROM users
            GROUP BY city
            ORDER BY user_count DESC, city ASC
            """,
            connection,
        )

    print(f"SQLite database saved to: {DB_PATH}")
    print("\nUser count by city (SQL query):")
    print(summary.to_string(index=False))


def main():
    try:
        records = fetch_data()
    except (requests.RequestException, ValueError) as error:
        print(f"Could not fetch API data: {error}")
        print("Please check your internet connection and run the program again.")
        return

    df = transform_data(records)
    save_to_csv(df)
    save_to_sqlite(df)
    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
