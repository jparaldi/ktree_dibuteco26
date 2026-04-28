from dash import Input, Output, State, html
import dash_leaflet as dl

from src.utils.csv_loader import load_points_from_csv
from src.core.kdtree import build_kdtree
from src.core.range_search import range_search, circular_range_search
from src.core.geometry import sort_by_distance
from src.services.geocoding import geocode_address

points = load_points_from_csv("data/processed/butecos_geocoded.csv")
tree = build_kdtree(points)

user_icon = {
    "iconUrl": "https://cdn-icons-png.flaticon.com/512/64/64113.png",
    "iconSize": [30, 30],
}

def register_callbacks(app):

    @app.callback(
        Output("results", "children"),
        Output("markers", "children"),
        Output("map", "center"),
        Input("search-button", "n_clicks"),
        State("address-input", "value"),
        State("top-n", "value"),
        State("custom-top-n", "value"),
        State("radius", "value"),
        State("custom-radius", "value"),
        State("use-circular", "value"),
    )
    def handle_search(
        n_clicks,
        address,
        top_n,
        custom_top_n,
        radius,
        custom_radius,
        use_circular,
    ):
        # evita que a função seja executada antes do primeiro clique
        if n_clicks == 0:
            return "", [], [-19.9208, -43.9378]
        
        #evita erro de input vazio
        if not address:
            return "Por favor, insira um endereço válido.", [], [-19.9208, -43.9378]
        
        # resolver top N
        if top_n == "custom":
            top_n = custom_top_n if custom_top_n else 5
        # garantir tipo correto para top_n
        top_n = int(top_n)

        # resolver raio
        if radius == "custom":
            radius = custom_radius if custom_radius else 2
        # garantir tipo correto para radius
        radius = float(radius)
        
        #1. Geocoding
        coords = geocode_address(address)
        if coords is None or coords[0] is None or coords[1] is None:
            return "Endereço não encontrado. Por favor, tente novamente.", [], [-19.9208, -43.9378]

        ref_lat, ref_lon = coords

        use_circular = use_circular or []
        is_circular = "circular" in use_circular

        #2 Busca na KD Tree
        if is_circular:
            results = circular_range_search(tree, ref_lat, ref_lon, radius)
        else:
            delta = radius / 111  # Aproximação: 1 grau ~ 111 km
            lat_min = ref_lat - delta
            lat_max = ref_lat + delta
            lon_min = ref_lon - delta
            lon_max = ref_lon + delta
            results = range_search(tree, lat_min, lat_max, lon_min, lon_max)

        if not results:
            return "Nenhum buteco encontrado próximo ao endereço fornecido.", [], [-19.9208, -43.9378]

        #4 Ordenação por distância
        sorted_results = sort_by_distance(results, ref_lat, ref_lon, metric="haversine")

        if is_circular:
            filtered = [(p, d) for p, d in sorted_results if d <= radius]

            if not filtered:
                return "Nenhum buteco encontrado dentro do raio especificado.", [], [-19.9208, -43.9378]

            top_results = filtered[:top_n]
        else:
            top_results = sorted_results[:top_n]
        
        result_text = html.Ul([
            html.Li(f"{p.name} -> {d:.2f} km") for p, d in top_results
        ])

        markers = []

        # Marcador do usuario
        markers.append(
            dl.Marker(
                position=(ref_lat, ref_lon),
                icon=user_icon,
                children=dl.Tooltip("Você está aqui"),
            )
        )

        # Marcadores dos butecos
        for p, d in top_results:
            # evitar erro com coordenadas inválidas
            if p.latitude is None or p.longitude is None:
                continue
            markers.append(
                dl.Marker(
                    position=(float(p.latitude), float(p.longitude)),
                    children=dl.Tooltip(f"{p.name} ({d:.2f} km)"),
                )
            )
        
        return result_text, markers, [ref_lat, ref_lon]