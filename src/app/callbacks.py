from dash import Input, Output, State, html
import dash_leaflet as dl

from src.utils.csv_loader import load_points_from_csv
from src.core.kdtree import build_kdtree
from src.core.range_search import range_search
from src.core.geometry import sort_by_distance
from src.services.geocoding import geocode_address

points = load_points_from_csv("data/processed/butecos_geocoded.csv")
tree = build_kdtree(points)

def register_callbacks(app):

    @app.callback(
        Output("results", "children"),
        Output("markers", "children"),
        Input("search-button", "n_clicks"),
        State("addres-input", "value")
    )
    def handle_search(n_clicks, address):
        # evita que a função seja executada antes do primeiro clique
        if n_clicks == 0:
            return "", []
        
        #evita erro de input vazio
        if not address:
            return "Por favor, insira um endereço válido.", []
        
        #1. Geocoding
        coords = geocode_address(address)
        if not coords:
            return "Endereço não encontrado. Por favor, tente novamente.", []
        
        ref_lat, ref_lon = coords

        #2 Bounding box
        delta = 0.02
        lat_min = ref_lat - delta
        lat_max = ref_lat + delta
        lon_min = ref_lon - delta
        lon_max = ref_lon + delta

        #3 Busca na KD Tree
        results = range_search(tree, lat_min, lat_max, lon_min, lon_max)

        if not results:
            return "Nenhum buteco encontrado próximo ao endereço fornecido.", []

        #4 Ordenação por distância
        sorted_results = sort_by_distance(results, ref_lat, ref_lon, metric="haversine")

        #5 Montar o top 5
        top5 = sorted_results[:5]
        if not top5:
            return "Nenhum buteco encontrado próximo ao endereço fornecido."
        
        result_text = html.Ul([
            html.Li(f"{p.name} -> {d:.2f} km") for p, d in top5
        ])

        print("DEBUG TOP5:")
        for p, d in top5:
            print(p.name, p.latitude, p.longitude)

        markers = []

        # Marcador do usuario
        markers.append(
            dl.Marker(
                position=(ref_lat, ref_lon),
                children=dl.Tooltip("Você está aqui"),
            )
        )

        # Marcadores dos butecos
        for p, d in top5:
            markers.append(
                dl.Marker(
                    position=(float(p.latitude), float(p.longitude)),
                    children=dl.Tooltip(f"{p.name} ({d:.2f} km)"),
                )
            )
        
        return result_text, markers