import pandas as pd
from src.models.point import Point

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

def load_points_from_csv(filepath: str):
    df = pd.read_csv(filepath, sep=';')

    points = []

    for _, row in df.iterrows():
        # ignora linhas inválidas
        if pd.isna(row["latitude"]) or pd.isna(row["longitude"]):
            continue

        point = Point(
            id=_,
            name=row["name"],
            address=row["address"],
            latitude=row["latitude"],
            longitude=row["longitude"],
        )

        points.append(point)

    return points