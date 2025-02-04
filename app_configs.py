# app_configs.py
import os

# Flask & Dash Configuration
DEBUG = True
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000

# IBM Quantum API Token
IBM_QUANTUM_TOKEN = os.getenv("IBM_QUANTUM_TOKEN", "5b54ce7addff77e8d1a989bedf44c7263c89cebf4c9aadec493cc1ccbddf1122450d1c212ba3d032539cefacfc3cb95b8c54ff690433ceb6d18e50d0f8ba380f")

# Map Configuration
DEPOT_ADDRESS = "George Bush Intercontinental Airport, Houston, TX"  # IAH Airport
DISTANCE_RADIUS = 5000  # Search radius around the depot (in meters)

# Application Settings
APP_TITLE = "Multi-Vehicle Routing Optimization"
MAIN_HEADER = "Optimized Routing"
DESCRIPTION = "Optimize vehicle routes using IBM Qiskit and view the results on a map."

# Solver Options
SOLVER_OPTIONS = ["IBM Qiskit"]

# Theme Configuration
THEME_COLOR = "#074C91"
THEME_COLOR_SECONDARY = "#2A7DE1"

# Number of Vehicles (for sliders in UI)
NUM_VEHICLES = {
    "min": 1,
    "max": 10,
    "step": 1,
    "value": 4,
}

# Number of Client Locations
NUM_CLIENT_LOCATIONS = {
    "min": 5,
    "max": 50,
    "step": 5,
    "value": 10,
}
