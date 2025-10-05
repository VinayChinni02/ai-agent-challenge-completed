
# ruff: noqa: E402
import sys
import os
import pandas as pd

# 🔑 Ensure project root is on sys.path so we can import custom_parsers
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from custom_parsers.icici_parser import parse

def normalize(df):
    """
    Normalizes DataFrame for test comparison.
    Strips whitespace, converts numbers to string with 2 decimals,
    and sorts rows by Date and Description.
    """
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Description"] = df["Description"].str.strip()
    for col in ["Debit Amt", "Credit Amt", "Balance"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0).round(2)
    df = df.sort_values(by=["Date", "Description"]).reset_index(drop=True)
    return df


def test_parse_matches_csv():
    pdf_file = "data/icici/icici sample.pdf"
    csv_file = "data/icici/result.csv"

    got = parse(pdf_file)
    expected = pd.read_csv(csv_file)

    got = normalize(got)
    expected = normalize(expected)

    assert got.equals(expected)

