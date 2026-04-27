from dash import Dash
from src.app.layout import create_layout
from src.app.callbacks import register_callbacks

app = Dash(__name__)

app.layout = create_layout()

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)