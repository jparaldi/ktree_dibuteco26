from src.models.point import Point
from src.core.kdtree import build_kdtree
from src.core.range_search import range_search
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
    # 1. criar pontos
    points = load_points_from_csv("data/processed/butecos_geocoded.csv")

    print("Pontos:")
    for p in points:
        print(p)

    # 2. construir árvore
    tree = build_kdtree(points)

    print("\nRaiz da árvore:")
    print(tree)

    # 3. definir região de busca
    lat_min, lat_max = -20.0, -19.7
    lon_min, lon_max = -44.1, -43.7

    print("\nBuscando na região:")
    print(f"lat: [{lat_min}, {lat_max}]")
    print(f"lon: [{lon_min}, {lon_max}]")

    # 4. executar busca
    results = range_search(tree, lat_min, lat_max, lon_min, lon_max)

    # 5. mostrar resultados
    print("\nResultados:")
    for p in results:
        print(p)
    
    lats = [p.latitude for p in points]
    lons = [p.longitude for p in points]

    print(min(lats), max(lats))
    print(min(lons), max(lons))


if __name__ == "__main__":
    main()