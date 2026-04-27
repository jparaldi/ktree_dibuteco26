from dash import Dash
from src.app.layout import create_layout
from src.app.callbacks import register_callbacks
import os

# Caminho para a pasta assets na raiz do projeto
assets_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")

app = Dash(__name__, assets_folder=assets_folder, title="BUTECOS")

app.layout = create_layout()

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)