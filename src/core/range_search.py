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

