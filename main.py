from src.models.point import Point
from src.core.kdtree import build_kdtree
from src.core.range_search import range_search
from src.core.geometry import sort_by_distance
from src.utils.csv_loader import load_points_from_csv
from src.services.geocoding import geocode_address


def create_test_points():
    return [
        Point(1, "A", "", -19.9, -43.9),
        Point(2, "B", "", -19.8, -43.8),
        Point(3, "C", "", -19.7, -43.7),
        Point(4, "D", "", -19.85, -43.85),
        Point(5, "E", "", -19.75, -43.75),
    ]


def main():
    # 1. carregar pontos reais
    points = load_points_from_csv("data/processed/butecos_geocoded.csv")
    print(f"\nTotal de pontos carregados: {len(points)}")

    # 2. construir árvore
    tree = build_kdtree(points)
    print("\nKD-Tree construída com sucesso.")

    # 3. input do usuário
    address = input("\nDigite um endereço: ")

    coords = geocode_address(address)

    if coords is None:
        print("Endereço não encontrado.")
        return

    ref_lat, ref_lon = coords
    print(f"\nCoordenadas encontradas: ({ref_lat}, {ref_lon})")

    # 4. definir retângulo dinâmico (simples)
    delta = 0.02  # ~2km (aproximação)

    lat_min = ref_lat - delta
    lat_max = ref_lat + delta
    lon_min = ref_lon - delta
    lon_max = ref_lon + delta

    print("\nRegião de busca:")
    print(f"lat: [{lat_min}, {lat_max}]")
    print(f"lon: [{lon_min}, {lon_max}]")

    # 5. busca na KD-tree
    results = range_search(tree, lat_min, lat_max, lon_min, lon_max)

    print(f"\nTotal encontrados na região: {len(results)}")

    if not results:
        print("Nenhum bar encontrado nessa região.")
        return

    # 6. ordenação por distância (HAVERSINE)
    sorted_hav = sort_by_distance(results, ref_lat, ref_lon, metric="haversine")

    print("\nTop 5 mais próximos (Haversine):")
    for p, d in sorted_hav[:5]:
        print(f"{p.name} -> {d:.2f} km")

    # 7. ordenação por distância (EUCLIDIANA)
    sorted_euc = sort_by_distance(results, ref_lat, ref_lon, metric="euclidean")

    print("\nTop 5 mais próximos (Euclidiana):")
    for p, d in sorted_euc[:5]:
        print(f"{p.name} -> {d:.6f} (graus)")

    # 8. debug opcional
    lats = [p.latitude for p in points]
    lons = [p.longitude for p in points]

    print("\nDistribuição dos dados:")
    print(f"Latitude:  {min(lats)} até {max(lats)}")
    print(f"Longitude: {min(lons)} até {max(lons)}")


if __name__ == "__main__":
    main()