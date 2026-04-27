from dash import html, dcc
import dash_leaflet as dl

def create_layout():
    return html.Div([
        html.H1("Butecos de Belo Horizonte"),
        
        dcc.Input(
            id = "address-input",
            type = "text",
            placeholder = "Digite um endereço...",
            style={"width": "60%", "marginRight": "10px"}
        ),

        # Controle de top N resultados
        dcc.Dropdown(
            id="top-n",
            options=[
                {"label": "Top 3", "value": 3},
                {"label": "Top 5", "value": 5},
                {"label": "Top 10", "value": 10},
                {"label": "Personalizado", "value": "custom"},
            ],
            value=5,
            style={"width": "200px", "marginTop": "10px"}
        ),

        dcc.Input(
            id="custom-top-n",
            type="number",
            placeholder="N",
            style={"marginLeft": "10px"}
        ),

        # Controle de raio de busca
        dcc.Dropdown(
            id="radius",
            options=[
                {"label": "1 km", "value": 1},
                {"label": "2 km", "value": 2},
                {"label": "5 km", "value": 5},
                {"label": "Personalizado", "value": "custom"},
            ],
            value=2,
            style={"width": "200px", "marginTop": "10px"}
        ),

        dcc.Input(
            id="custom-radius",
            type="number",
            placeholder="km",
            style={"marginLeft": "10px"}
        ),

        html.Button("Pesquisar", id="search-button", n_clicks=0),

        html.Div(id="results", style={"marginTop": "20px"}),

        dl.Map(
            id="map",
            center=[-19.9208, -43.9378],
            zoom=13.95,
            children=[
                dl.TileLayer(),
                dl.LayerGroup(id="markers")# Onde entram os pontos
            ],
            style={"width": "100%", "height": "500px", "marginTop": "20px"}
        )
    ])