from dash import Dash, html, dcc, Input, Output, callback
from script import type_hex 
import webbrowser
import time

app = Dash(__name__)

app.layout = html.Div([
    html.Button("Generate ID", id="generate-btn", n_clicks=0),
    html.Div(id="output")
])

@callback(
    Output("output", "children"),
    Input("generate-btn", "n_clicks"),
    prevent_initial_call=True
)
def generate_id(n_clicks):
    type_hex()

def open_browser():
      webbrowser.open_new('http://127.0.0.1:8050/')

if __name__ == '__main__':
    open_browser()
    app.run(port=8050)
    