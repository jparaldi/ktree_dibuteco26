import pandas as pd

def load_bars_csv(filepath: str):
    df = pd.read_csv(filepath, sep=';')

    records = []

    for idx, row in df.itterrows():
        record = {
            "id": idx,
            "name": str(row["name"]).strip(),
            "address": str(row["address"]).strip(),
        }
        records.append(record)

    return records