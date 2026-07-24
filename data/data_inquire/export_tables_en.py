"""
Export SQL analysis results to a multi-sheet Excel workbook.

Usage:
    python export_tables_en.py
    (Requires dropout_tables_EN.xlsx to exist from prior SQL exports.)
"""
import pandas as pd
import os

EXCEL_IN = "dropout_tables_EN.xlsx"
EXCEL_OUT = "dropout_tables_EN.xlsx"


def main():
    if not os.path.exists(EXCEL_IN):
        print(f"Input file '{EXCEL_IN}' not found. Run SQL queries first to generate it.")
        return

    # Read existing workbook
    sheets = pd.read_excel(EXCEL_IN, sheet_name=None)
    print(f"Read {len(sheets)} sheet(s) from {EXCEL_IN}: {list(sheets.keys())}")

    # Standardise column names across sheets
    for name, df in sheets.items():
        df.columns = [str(c).strip() for c in df.columns]
        print(f"  Sheet '{name}': {len(df)} rows, cols={list(df.columns)}")

    # Write back
    with pd.ExcelWriter(EXCEL_OUT, engine="openpyxl") as w:
        for name, df in sheets.items():
            df.to_excel(w, sheet_name=name, index=False)
    print(f"Done  -> {os.path.abspath(EXCEL_OUT)}")


if __name__ == "__main__":
    main()
