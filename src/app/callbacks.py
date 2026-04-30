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
    "iconUrl": "/assets/user_icon.png",
    "iconSize": [40, 40],
}

bar_icon = {
    "iconUrl": "/assets/bar_icon.png",
    "iconSize": [40, 40],
}

def register_callbacks(app):
    # Modal de opções
    @app.callback(
        Output("options-modal", "style"),
        Input("options-button", "n_clicks"),
        Input("close-options-button", "n_clicks"),
        State("options-modal", "style"),
        prevent_initial_call=False,
    )
    def toggle_options_modal(open_clicks, close_clicks, current_style):
        if not open_clicks:
            return current_style or {"display": "none"}

        modal_display = current_style.get("display", "none") if current_style else "none"
        new_display = "none" if modal_display != "none" else "flex"
        
        # Se está fechando, retorna none
        if close_clicks and close_clicks > open_clicks:
            new_display = "none"

        return {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "right": 0,
            "bottom": 0,
            "backgroundColor": "rgba(0, 0, 0, 0.5)",
            "display": new_display,
            "justifyContent": "center",
            "alignItems": "center",
            "zIndex": 2000,
        }

    # Sincronizar address input
    @app.callback(
        Output("address-input", "value"),
        Input("address-input-field", "value"),
    )
    def update_address_input(field_value):
        return field_value or ""

    # Sincronizar sliders com inputs hidden
    @app.callback(
        Output("top-n", "value"),
        Output("radius", "value"),
        Input("top-n-slider", "value"),
        Input("radius-slider", "value"),
    )
    def update_hidden_values(top_n_val, radius_val):
        return top_n_val, radius_val

    @app.callback(
    Output("landing-screen", "style"),
    Output("main-app", "style"),
    Input("start-button", "n_clicks"),
)
    def show_app(n_clicks):
        if n_clicks == 0:
            return (
                {
                    "height": "100vh",
                    "width": "100vw",
                    "backgroundImage": "url('/assets/background.jpg')",
                    "backgroundSize": "cover",
                    "backgroundPosition": "center",
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                },
                {"display": "none"}
            )

        return (
            {"display": "none"},
            {
                "position": "fixed",
                "inset": 0,
                "width": "100vw",
                "height": "100vh",
                "overflow": "auto",
                "visibility": "visible",
                "opacity": 1,
                "pointerEvents": "auto",
            }
        )


    @app.callback(
        Output("results", "children"),
        Output("markers", "children"),
        Output("search-area", "children"),
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
            return html.Div(
                "🔍 Digite um endereço e clique em 'Pesquisar'",
                style={"textAlign": "center", "color": "#999", "paddingTop": "40px"}
            ), [], [], [-19.9208, -43.9378]
        
        #evita erro de input vazio
        if not address:
            return html.Div(
                "⚠️ Endereço inválido",
                style={"color": "#d32f2f", "fontWeight": "bold"}
            ), [], [], [-19.9208, -43.9378]
        
        # resolver top N
        # garantir tipo correto para top_n
        top_n = int(top_n)
        top_n = max(1, min(127, top_n))

        # resolver raio
        # garantir tipo correto para radius
        radius = float(radius)
        
        #1. Geocoding
        coords = geocode_address(address)
        if coords is None or coords[0] is None or coords[1] is None:
            return html.Div(
                "❌ Endereço não encontrado",
                style={"color": "#d32f2f", "fontWeight": "bold"}
            ), [], [], [-19.9208, -43.9378]

        ref_lat, ref_lon = coords

        use_circular = use_circular or []
        is_circular = "circular" in use_circular

        #2 Busca na KD Tree
        if is_circular:
            search_area = [
                dl.Circle(
                    center=(ref_lat, ref_lon),
                    radius=radius * 1000,
                    color="#ff6600",
                    fillColor="#ff6600",
                    fillOpacity=0.15,
                    weight=2,
                )
            ]
            results = circular_range_search(tree, ref_lat, ref_lon, radius)
        else:
            delta = radius / 111  # Aproximação: 1 grau ~ 111 km
            lat_min = ref_lat - delta
            lat_max = ref_lat + delta
            lon_min = ref_lon - delta
            lon_max = ref_lon + delta
            search_area = [
                dl.Rectangle(
                    bounds=((lat_min, lon_min), (lat_max, lon_max)),
                    color="#ff6600",
                    fillColor="#ff6600",
                    fillOpacity=0.15,
                    weight=2,
                )
            ]
            results = range_search(tree, lat_min, lat_max, lon_min, lon_max)

        if not results:
            return html.Div(
                "😞 Nenhum buteco encontrado",
                style={"color": "#ff9800", "fontWeight": "bold"}
            ), [], search_area, [ref_lat, ref_lon]

        #4 Ordenação por distância
        sorted_results = sort_by_distance(results, ref_lat, ref_lon, metric="haversine")

        if is_circular:
            filtered = [(p, d) for p, d in sorted_results if d <= radius]

            top_results = filtered[:top_n]
        else:
            top_results = sorted_results[:top_n]
        
        result_items = []
        for idx, (p, d) in enumerate(top_results, 1):
            result_items.append(
                html.Div([
                    html.Div(
                        f"{idx}. {p.name}",
                        style={
                            "fontWeight": "bold",
                            "fontSize": "16px",
                            "color": "#ff6600",
                            "marginBottom": "4px",
                        }
                    ),
                    html.Div(
                        f"📍 {d:.2f} km",
                        style={
                            "fontSize": "13px",
                            "color": "#666",
                            "marginBottom": "12px",
                        }
                    ),
                ],
                style={
                    "paddingBottom": "12px",
                    "borderBottom": "1px solid #eee",
                }
                )
            )

        result_text = html.Div([
            html.Div(
                f"✓ Encontrados {len(top_results)} buteco(s)",
                style={
                    "fontWeight": "bold",
                    "fontSize": "15px",
                    "color": "#4caf50",
                    "marginBottom": "16px",
                    "paddingBottom": "12px",
                    "borderBottom": "2px solid #4caf50",
                }
            ),
            html.Div(result_items),
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
                    icon=bar_icon,
                    children=dl.Tooltip(f"{p.name} ({d:.2f} km)"),
                )
            )
        
        return result_text, markers, search_area, [ref_lat, ref_lon]

    # Reset das opções
    @app.callback(
        Output("top-n-slider", "value"),
        Output("radius-slider", "value"),
        Output("use-circular", "value"),
        Input("reset-button", "n_clicks"),
        prevent_initial_call=True,
    )
    def reset_options(n_clicks):
        return 5, 2, []
        
        return result_text, markers, search_area, [ref_lat, ref_lon]