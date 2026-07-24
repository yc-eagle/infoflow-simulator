import sqlite3
import os

DB = "seed710_2000.db"

SQL_FILES = [
    "basic_CET.sql",
    "density_dropout.sql",
    "familiarity_dropout.sql"
]

def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    for sql_file in SQL_FILES:
        print("Running:", sql_file)
        with open(sql_file, "r", encoding="utf-8") as f:
            cur.executescript(f.read())
        print("  Done:", sql_file)

    conn.commit()
    conn.close()
    print("\nAll 3 tables created successfully!")

if __name__ == "__main__":
    main()
