import sqlite3
import pandas as pd
from config import DATABASE

def connect():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def run_query(query):

    conn = connect()
    cur = conn.cursor()

    try:

        cur.execute(query)

        if query.lower().startswith("select"):

            rows = cur.fetchall()

            columns = [c[0] for c in cur.description]

            data = [list(r) for r in rows]

            return columns, data

        else:

            conn.commit()
            return [], []

    finally:

        conn.close()


def list_tables():

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )

    tables = [r[0] for r in cur.fetchall()]

    conn.close()

    return tables


def get_table(table):

    conn = connect()

    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)

    conn.close()

    return df.columns.tolist(), df.values.tolist()


def insert_row(table, data):

    conn = connect()

    cols = ",".join(data.keys())
    vals = ",".join(["?"] * len(data))

    sql = f"INSERT INTO {table} ({cols}) VALUES ({vals})"

    conn.execute(sql, list(data.values()))

    conn.commit()
    conn.close()


def delete_row(table, rowid):

    conn = connect()

    conn.execute(f"DELETE FROM {table} WHERE rowid={rowid}")

    conn.commit()

    conn.close()


def export_csv(table):

    conn = connect()

    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)

    file = f"{table}.csv"

    df.to_csv(file, index=False)

    conn.close()

    return file
