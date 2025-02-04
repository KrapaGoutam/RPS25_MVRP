# app.py
from flask import Flask, request, jsonify
import folium
from map import get_map
from solver import solve_mvrp
from app_configs import SOLVER_OPTIONS
from dash_html import create_dash_app
import threading

# Initialize Flask server
server = Flask(__name__)

# Get port settings
FLASK_PORT = 5000
DASH_PORT = 8050

# Create Dash app inside Flask
dash_app = create_dash_app(server)

@server.route("/generate_map", methods=["POST"])
def generate_map():
    """Handles route optimization and map generation."""
    data = request.get_json()
    solver = data.get("solver")
    num_vehicles = data.get("num_vehicles")
    num_clients = data.get("num_clients")

    if solver not in SOLVER_OPTIONS:
        return jsonify({"error": "Invalid solver selected!"}), 400

    # Generate map and solve routing problem
    initial_map, locations, G = get_map()
    optimized_routes = solve_mvrp(locations[:num_clients], G, num_vehicles)

    # Plot optimized routes
    for route in optimized_routes:
        folium.PolyLine(route, color="blue", weight=2.5).add_to(initial_map)

    # Save and return updated map
    map_path = "static/optimized_map.html"
    initial_map.save(map_path)

    return jsonify({"map_url": f"/{map_path}"})


def run_dash():
    """Runs the Dash UI in the same Flask context."""
    dash_app.run(host="0.0.0.0", port=DASH_PORT, debug=False, use_reloader=False)


if __name__ == "__main__":
    # Start Dash UI in a separate thread
    dash_thread = threading.Thread(target=run_dash)
    dash_thread.daemon = True
    dash_thread.start()

    # Start Flask API
    server.run(debug=True, host="0.0.0.0", port=FLASK_PORT)
