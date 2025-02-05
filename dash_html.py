import time
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import requests
from app_configs import *

def create_dash_app(flask_server):
    """Creates the Dash UI as a dashboard within Flask."""
    dash_app = dash.Dash(__name__, server=flask_server, routes_pathname_prefix="/")

    dash_app.layout = html.Div([
        html.H1(MAIN_HEADER),
        html.P(DESCRIPTION),

        html.Label("Choose Solver:"),
        dcc.Dropdown(
            id="solver-dropdown",
            options=[{"label": solver, "value": solver} for solver in SOLVER_OPTIONS],
            value=SOLVER_OPTIONS[0],
            clearable=False
        ),

        html.Label("Number of Vehicles:"),
        dcc.Slider(id="num-vehicles", min=NUM_VEHICLES["min"], max=NUM_VEHICLES["max"],
                   step=NUM_VEHICLES["step"], value=NUM_VEHICLES["value"],
                   marks={i: str(i) for i in range(NUM_VEHICLES["min"], NUM_VEHICLES["max"]+1)}),

        html.Label("Number of Client Locations:"),
        dcc.Slider(id="num-clients", min=NUM_CLIENT_LOCATIONS["min"], max=NUM_CLIENT_LOCATIONS["max"],
                   step=NUM_CLIENT_LOCATIONS["step"], value=NUM_CLIENT_LOCATIONS["value"],
                   marks={i: str(i) for i in range(NUM_CLIENT_LOCATIONS["min"], NUM_CLIENT_LOCATIONS["max"]+1)}),

        html.Button("Optimize Routes", id="run-button", n_clicks=0),

        html.Iframe(id="map-display", src="/static/optimized_map.html", width="800", height="500"),

        html.Div(id="output-status")
    ])

    @dash_app.callback(
        Output("map-display", "src"),
        Output("output-status", "children"),
        Input("run-button", "n_clicks"),
        State("solver-dropdown", "value"),
        State("num-vehicles", "value"),
        State("num-clients", "value")
    )
    def optimize_routes(n_clicks, solver, num_vehicles, num_clients):
        if n_clicks > 0:
            try:
                response = requests.post("http://127.0.0.1:5000/generate_map", json={
                    "solver": solver,
                    "num_vehicles": num_vehicles,
                    "num_clients": num_clients
                })

                if response.status_code != 200:
                    error_message = response.json().get('error', 'Unknown error')
                    print(f"⚠ API Error: {error_message}")
                    return "/static/optimized_map.html", f"❌ Error: {error_message}"

                data = response.json()
                print(f"✅ Dash received updated map: {data['map_url']}")

                # Force refresh by adding a timestamp to the URL
                new_map_url = f"{data['map_url']}?t={int(time.time())}"
                return new_map_url, "✅ Optimization Complete! Map Updated."

            except requests.exceptions.RequestException as e:
                print(f"❌ API Request Failed: {e}")
                return "/static/optimized_map.html", "❌ API Connection Error. Is Flask running?"
        
        return "/static/optimized_map.html", "⏳ Waiting for optimization..."

    return dash_app
