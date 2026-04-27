from dash import html, dcc
import dash_leaflet as dl

def create_layout():
    return html.Div([
        html.H1("Butecos de Belo Horizonte"),
        
        dcc.Input(
            id = "addres-input",
            type = "text",
            placeholder = "Digite um endereço...",
            style={"width": "60%", "marginRight": "10px"}
        ),

        html.Button("Pesquisar", id="search-button", n_clicks=0),

        html.Div(id="results", style={"marginTop": "20px"}),

        dl.Map(
            id="map",
            center=[-19.9208, -43.9378],
            zoom=12,
            children=[
                dl.TileLayer(),
                dl.LayerGroup(id="markers")# Onde entram os pontos
            ],
            style={"width": "100%", "height": "500px", "marginTop": "20px"}
        )
    ])