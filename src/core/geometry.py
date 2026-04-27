from src.services.distance import haversine

def sort_by_distance(points, ref_lat, ref_lon, metric='haversine'):
    if metric == 'haversine':
        from src.services.distance import haversine as dist
    elif metric == 'euclidean':
        from src.services.distance import euclidean as dist
    else:
        raise ValueError("Métrica desconhecida. Use 'haversine' ou 'euclidean'.")

    # cria lista de tuplas (distância, ponto)
    points_with_dist = []

    for p in points:
        d = dist(ref_lat, ref_lon, p.latitude, p.longitude)
        points_with_dist.append((p, d))

    # ordena pela distância
    points_with_dist.sort(key=lambda x: x[1])

    return points_with_dist