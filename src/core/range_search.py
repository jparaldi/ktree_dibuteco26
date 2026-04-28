from src.services.distance import haversine


def range_search(node, lat_min, lat_max, lon_min, lon_max, results=None):
    if results is None:
        results = []

    if not node:
        return results
    
    point = node.point
    lat = point.latitude
    lon = point.longitude

    #1 checa se esta dentro do retangulo

    if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
        results.append(point)
    
    axis = node.axis

    #2 decide qual lado do nodo explorar primeiro
    if axis == 0: #latitude
        if lat_min <= lat:
            range_search(node.left, lat_min, lat_max, lon_min, lon_max, results)
        if lat <= lat_max:
            range_search(node.right, lat_min, lat_max, lon_min, lon_max, results)
    
    if axis == 1: #longitude
        if lon_min <= lon:
            range_search(node.left, lat_min, lat_max, lon_min, lon_max, results)
        if lon <= lon_max:
            range_search(node.right, lat_min, lat_max, lon_min, lon_max, results)
    
    return results


def circular_range_search(node, center_lat, center_lon, radius_km, results=None):
    if results is None:
        results = []

    if not node:
        return results

    point = node.point
    lat = point.latitude
    lon = point.longitude

    #1 checa se esta dentro do circulo
    if point.distance_to(center_lat, center_lon) <= radius_km:
        results.append(point)

    axis = node.axis

    #2 decide qual lado do nodo explorar primeiro
    if axis == 0:  # latitude
        if center_lat < lat:
            close_branch = node.left
            far_branch = node.right
        else:
            close_branch = node.right
            far_branch = node.left

        circular_range_search(close_branch, center_lat, center_lon, radius_km, results)

        split_distance = haversine(center_lat, center_lon, lat, center_lon)
        if split_distance < radius_km:
            circular_range_search(far_branch, center_lat, center_lon, radius_km, results)

    if axis == 1:  # longitude
        if center_lon < lon:
            close_branch = node.left
            far_branch = node.right
        else:
            close_branch = node.right
            far_branch = node.left

        circular_range_search(close_branch, center_lat, center_lon, radius_km, results)

        split_distance = haversine(center_lat, center_lon, center_lat, lon)
        if split_distance < radius_km:
            circular_range_search(far_branch, center_lat, center_lon, radius_km, results)

    return results