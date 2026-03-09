import sqlite3
import pandas as pd
from config import DATABASE

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def run_query(query):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query)

        if query.strip().lower().startswith("select"):
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

            data = []
            for row in rows:
                data.append(list(row))

            return columns, data
        else:
            conn.commit()
            return [], []

    finally:
        conn.close()


def list_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )

    tables = [row[0] for row in cursor.fetchall()]

    conn.close()
    return tables


def export_csv(table):
    conn = get_connection()

    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)

    file = f"{table}.csv"
    df.to_csv(file, index=False)

    conn.close()

    return file
