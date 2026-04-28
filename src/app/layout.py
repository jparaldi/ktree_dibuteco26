from dash import html, dcc
import dash_leaflet as dl

def create_layout():
    return html.Div([
        html.Div(
            id="landing-screen",
            children=[
                html.Div(
                    [
                        html.H1("🍺 MELHOR ENCONTRADOR DE BUTECOS DE BH 🍻"),
                        html.P("😍Encontre os melhores butecos próximos de você.😍"),
                        html.Button(
                            "Começar",
                            id="start-button",
                            n_clicks=0,
                            style={
                                "padding": "20px 40px",
                                "fontSize": "24px",
                                "backgroundColor": "#ff6600",
                                "color": "white",
                                "border": "none",
                                "borderRadius": "10px",
                                "cursor": "pointer",
                            }
                        ),
                    ],
                    style={
                        "backgroundColor": "rgba(0, 0, 0, 0.55)",
                        "padding": "32px",
                        "borderRadius": "18px",
                        "textAlign": "center",
                        "color": "white",
                    },
                )
            ],
            style={
                "height": "100vh",
                "width": "100vw",
                "backgroundImage": "url('/assets/background.jpg')",
                "backgroundSize": "cover",
                "backgroundPosition": "center",
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
            },
        ),

        html.Div(
            id="main-app",
            children=[
                html.Div(
                    [
                        dcc.Input(
                            id="address-input-field",
                            type="text",
                            placeholder="Digite um endereço ou local...",
                            style={
                                "flex": 1,
                                "minWidth": "520px",
                                "maxWidth": "1200px",
                                "height": "48px",
                                "padding": "10px 20px",
                                "fontSize": "18px",
                                "lineHeight": "20px",
                                "border": "2px solid #e0e0e0",
                                "borderRadius": "10px",
                                "outline": "none",
                                "fontFamily": "Arial, sans-serif",
                                "boxSizing": "border-box",
                                "backgroundColor": "#fff",
                                "verticalAlign": "middle",
                            }
                        ),
                        html.Button(
                            "Pesquisar",
                            id="search-button",
                            n_clicks=0,
                            style={
                                "marginLeft": "12px",
                                "padding": "14px 28px",
                                "fontSize": "16px",
                                "fontWeight": "bold",
                                "backgroundColor": "#ff6600",
                                "color": "white",
                                "border": "none",
                                "borderRadius": "8px",
                                "cursor": "pointer",
                                "transition": "background-color 0.3s",
                                "whiteSpace": "nowrap",
                            }
                        ),
                        html.Button(
                            "Opções",
                            id="options-button",
                            n_clicks=0,
                            style={
                                "marginLeft": "8px",
                                "padding": "14px 24px",
                                "fontSize": "16px",
                                "fontWeight": "bold",
                                "backgroundColor": "#333",
                                "color": "white",
                                "border": "none",
                                "borderRadius": "8px",
                                "cursor": "pointer",
                                "transition": "background-color 0.3s",
                                "whiteSpace": "nowrap",
                            }
                        ),
                    ],
                    style={
                        "position": "fixed",
                        "top": 0,
                        "left": 0,
                        "right": 0,
                        "zIndex": 1000,
                        "display": "flex",
                        "gap": "8px",
                        "padding": "16px 20px",
                        "backgroundColor": "white",
                        "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                        "boxSizing": "border-box",
                    }
                ),

                html.Div(
                    id="options-modal",
                    children=[
                        html.Div(
                            [
                                html.H2("Opções de Busca", style={"marginTop": 0}),
                                html.Hr(style={"margin": "16px 0"}),

                                html.Label("Quantidade de Resultados:", style={"fontWeight": "bold", "display": "block", "marginBottom": "8px"}),
                                html.Div(
                                    dcc.Slider(
                                        id="top-n-slider",
                                        min=1,
                                        max=20,
                                        value=5,
                                        marks={i: str(i) for i in range(1, 21)},
                                        tooltip={"placement": "bottom", "always_visible": True},
                                    ),
                                    style={"marginBottom": "24px"}
                                ),

                                html.Label("Raio de Busca (km):", style={"fontWeight": "bold", "display": "block", "marginBottom": "8px"}),
                                html.Div(
                                    dcc.Slider(
                                        id="radius-slider",
                                        min=0.5,
                                        max=10,
                                        step=0.5,
                                        value=2,
                                        marks={i: f"{i}km" for i in [0.5, 1, 2, 5, 10]},
                                        tooltip={"placement": "bottom", "always_visible": True},
                                    ),
                                    style={"marginBottom": "24px"}
                                ),
                                dcc.Checklist(
                                    id="use-circular",
                                    options=[{"label": "Busca circular", "value": "circular"}],
                                    value=[],
                                    style={"marginTop": "10px"}
                                ),

                                html.Button(
                                    "Fechar",
                                    id="close-options-button",
                                    style={
                                        "width": "100%",
                                        "padding": "12px",
                                        "fontSize": "16px",
                                        "fontWeight": "bold",
                                        "backgroundColor": "#ff6600",
                                        "color": "white",
                                        "border": "none",
                                        "borderRadius": "8px",
                                        "cursor": "pointer",
                                    }
                                ),
                            ],
                            style={
                                "backgroundColor": "white",
                                "padding": "24px",
                                "borderRadius": "12px",
                                "boxShadow": "0 4px 16px rgba(0, 0, 0, 0.2)",
                                "maxWidth": "400px",
                                "width": "90%",
                            }
                        )
                    ],
                    style={
                        "position": "fixed",
                        "top": 0,
                        "left": 0,
                        "right": 0,
                        "bottom": 0,
                        "backgroundColor": "rgba(0, 0, 0, 0.5)",
                        "display": "none",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "zIndex": 2000,
                    }
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                dl.Map(
                                    id="map",
                                    center=[-19.9208, -43.9378],
                                    zoom=13.95,
                                    children=[
                                        dl.TileLayer(),
                                        dl.LayerGroup(id="search-area"),
                                        dl.LayerGroup(id="markers"),
                                    ],
                                    style={"width": "100%", "height": "100%"},
                                ),
                            ],
                            style={
                                "flex": 1,
                                "borderRadius": "12px",
                                "overflow": "hidden",
                                "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.15)",
                                "backgroundColor": "#1a1a1a",
                            }
                        ),

                        html.Div(
                            id="results",
                            style={
                                "width": "320px",
                                "overflowY": "auto",
                                "padding": "20px",
                                "backgroundColor": "white",
                                "borderRadius": "12px",
                                "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
                                "fontSize": "14px",
                            }
                        ),
                    ],
                    style={
                        "display": "flex",
                        "gap": "16px",
                        "marginTop": "76px",
                        "marginBottom": "100px",
                        "marginLeft": "20px",
                        "marginRight": "20px",
                        "height": "calc(100vh - 176px)",
                        "boxSizing": "border-box",
                    }
                ),

                html.Div(
                    [
                        html.Div([
                            html.Img(src="/assets/user_icon.png", style={"width": "24px", "height": "24px", "marginRight": "8px"}),
                            html.Span("Sua Localização", style={"fontWeight": "bold"}),
                        ], style={"display": "flex", "alignItems": "center", "marginRight": "24px"}),

                        html.Div([
                            html.Img(src="/assets/bar_icon.png", style={"width": "24px", "height": "24px", "marginRight": "8px"}),
                            html.Span("Buteco", style={"fontWeight": "bold"}),
                        ], style={"display": "flex", "alignItems": "center"}),
                    ],
                    style={
                        "position": "fixed",
                        "bottom": "16px",
                        "left": "20px",
                        "display": "flex",
                        "gap": "16px",
                        "padding": "12px 16px",
                        "backgroundColor": "white",
                        "borderRadius": "8px",
                        "boxShadow": "0 2px 8px rgba(0, 0, 0, 0.1)",
                        "fontSize": "13px",
                        "zIndex": 100,
                    }
                ),

                dcc.Input(id="address-input", type="hidden", value=""),
                dcc.Input(id="top-n", type="hidden", value=5),
                dcc.Input(id="radius", type="hidden", value=2),
                dcc.Input(id="custom-top-n", type="hidden", value=None),
                dcc.Input(id="custom-radius", type="hidden", value=None),
            ],
            style={
                "position": "fixed",
                "inset": 0,
                "width": "100vw",
                "height": "100vh",
                "overflow": "auto",
                "visibility": "hidden",
                "opacity": 0,
                "pointerEvents": "none",
                "backgroundColor": "#fafafa",
            },
        )
    ])