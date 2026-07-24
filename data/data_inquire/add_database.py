"""
Import a behavioral-telemetry CSV into a SQLite database.

Usage:
    python add_database.py [csv_path] [db_path]

Defaults:
    csv_path = seed710_2000sample.csv
    db_path  = seed710_2000.db
"""
import sqlite3
import pandas as pd
import os
import sys


def csv_to_sqlite(csv_path: str, db_path: str, table_name: str = "behavior_logs"):
    """Read a CSV and write it into a SQLite table, replacing if it exists."""
    print(f"Reading: {csv_path}")
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    print(f"  → {len(df):,} rows × {len(df.columns)} columns")

    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    size_kb = os.path.getsize(db_path) / 1024
    print(f"  → Written to {db_path} ({size_kb:.1f} KB, table: {table_name})")
    print("Done.")


if __name__ == "__main__":
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "seed710_2000sample.csv"
    db_file = sys.argv[2] if len(sys.argv) > 2 else "seed710_2000.db"
    csv_to_sqlite(csv_file, db_file)
