from geopy.geocoders import Nominatim
import time
import pandas as pd

geolocator = Nominatim(user_agent="meu_geocoder_tp1")


def geocode_address(address: str):
    location = geolocator.geocode(address)

    if location:
        return location.latitude, location.longitude

    simplified = address.split(",")
    
    if len(simplified) >= 3:
        simplified_address = ",".join(simplified[:3])
    else:
        simplified_address = address

    location = geolocator.geocode(simplified_address)

    if location:
        return location.latitude, location.longitude

    return None, None

def geocode_csv(input_path:str, output_path:str):
    df = pd.read_csv(input_path, sep=';')

    latitudes = []
    longitudes = []

    for i, row in df.iterrows():
        address = row["address"]

        print(f"Geocoding address: {address}")

        lat, lon = geocode_address(address)

        latitudes.append(lat)
        longitudes.append(lon)

        time.sleep(1)

    df["latitude"] = latitudes
    df["longitude"] = longitudes

    df.to_csv(output_path, sep=';', index=False)

    print(f"Geocoding completo. Salvo em {output_path}")

def validate_geocoded_csv(filepath: str):
    df = pd.read_csv(filepath, sep=';')

    valid = []
    invalid = []

    for _, row in df.iterrows():
        lat = row["latitude"]
        lon = row["longitude"]

        # checagem básica
        if pd.isna(lat) or pd.isna(lon):
            invalid.append(row)
            continue

        if not (-21 < lat < -18 and -45 < lon < -42):
            invalid.append(row)
            continue

        valid.append(row)

    print(f"Total: {len(df)}")
    print(f"Válidos: {len(valid)}")
    print(f"Inválidos: {len(invalid)}")

    return valid, invalid

if __name__ == "__main__":
    geocode_csv("../../data/raw/gemni_butecos.csv", "../../data/processed/butecos_geocoded.csv")
    validate_geocoded_csv("../../data/processed/butecos_geocoded.csv")
