
import pandas as pd
import pdfplumber

COLUMNS = ['Date', 'Description', 'Debit Amt', 'Credit Amt', 'Balance']

def parse(pdf_path: str) -> pd.DataFrame:
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table[1:]:  # skip header row
                    if row and len(row) == len(COLUMNS):
                        rows.append(row)
    return pd.DataFrame(rows, columns=COLUMNS)
