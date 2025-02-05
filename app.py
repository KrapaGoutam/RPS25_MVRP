import os
import time
import socket
from flask import Flask, request, jsonify, send_from_directory
import folium
from map import get_map
from solver import solve_mvrp
from app_configs import SOLVER_OPTIONS
from dash_html import create_dash_app
import threading

# Function to find an available port
def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    _, port = s.getsockname()
    s.close()
    return port

# Set dynamic ports if default ones are in use
FLASK_PORT = int(os.environ.get("PORT", 5000))
DASH_PORT = 8050

# Initialize Flask server
server = Flask(__name__)

# Create Dash app inside Flask
dash_app = create_dash_app(server)

@server.route("/generate_map", methods=["POST"])
def generate_map():
    """Handles route optimization and map generation."""
    try:
        data = request.get_json()
        print("🔍 Received request data:", data)

        if not data:
            return jsonify({"error": "Invalid request: No data received"}), 400

        solver = data.get("solver")
        num_vehicles = data.get("num_vehicles")
        num_clients = data.get("num_clients")

        if solver not in SOLVER_OPTIONS:
            return jsonify({"error": f"Invalid solver selected: {solver}"}), 400

        print(f"🚀 Running optimization with {num_vehicles} vehicles and {num_clients} clients.")

        # Generate map and solve routing problem
        initial_map, locations, G = get_map()
        optimized_routes = solve_mvrp(locations[:num_clients], G, num_vehicles)

        print(f"✅ Optimization completed. Routes: {optimized_routes}")

        # Plot optimized routes
        for route in optimized_routes:
            folium.PolyLine(route, color="blue", weight=2.5).add_to(initial_map)

        # Save updated map
        map_path = "static/optimized_map.html"
        initial_map.save(map_path)

        print(f"✅ Map updated successfully: {map_path}")

        return jsonify({"map_url": f"/{map_path}"})

    except Exception as e:
        print(f"❌ Error processing request: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@server.route('/static/<path:filename>')
def static_files(filename):
    """Ensures Flask serves files from the static directory."""
    return send_from_directory(os.path.join(os.getcwd(), 'static'), filename)

def run_dash():
    """Runs the Dash UI in the same Flask context."""
    dash_app.run(host="0.0.0.0", port=DASH_PORT, debug=False, use_reloader=False)

if __name__ == "__main__":
    print(f"🌍 Flask running on http://127.0.0.1:{FLASK_PORT}/")
    print(f"📊 Dash running on http://127.0.0.1:{DASH_PORT}/")

    # Start Dash UI in a separate thread
    dash_thread = threading.Thread(target=run_dash)
    dash_thread.daemon = True
    dash_thread.start()

    # Start Flask API
    server.run(debug=True, host="0.0.0.0", port=FLASK_PORT)
