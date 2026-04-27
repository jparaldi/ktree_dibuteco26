from src.models.point import Point
from src.core.kdtree import build_kdtree
from src.core.range_search import range_search
from src.core.geometry import sort_by_distance
from src.utils.csv_loader import load_points_from_csv


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

    print("\nRaiz da árvore:")
    print(tree)

    # 3. definir região de busca (ampla pra garantir retorno)
    lat_min, lat_max = -20.0, -19.7
    lon_min, lon_max = -44.1, -43.7

    print("\nBuscando na região:")
    print(f"lat: [{lat_min}, {lat_max}]")
    print(f"lon: [{lon_min}, {lon_max}]")

    # 4. busca na KD-tree
    results = range_search(tree, lat_min, lat_max, lon_min, lon_max)

    print(f"\nTotal encontrados: {len(results)}")

    # 5. ponto de referência (simula usuário)
    ref_lat, ref_lon = -19.9, -43.9

    print(f"\nPonto de referência: ({ref_lat}, {ref_lon})")

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

    # 8. debug da distribuição dos dados
    lats = [p.latitude for p in points]
    lons = [p.longitude for p in points]

    print("\nDistribuição dos dados:")
    print(f"Latitude:  {min(lats)} até {max(lats)}")
    print(f"Longitude: {min(lons)} até {max(lons)}")


if __name__ == "__main__":
    main()