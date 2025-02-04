# map.py
import osmnx as ox
import folium
from app_configs import DEPOT_ADDRESS, DISTANCE_RADIUS

def get_map():
    """Fetches locations and creates an initial map."""
    # Get road network around depot
    G = ox.graph_from_address(DEPOT_ADDRESS, dist=DISTANCE_RADIUS, network_type="drive")
    
    # Select client locations
    nodes = list(G.nodes)[:10]
    locations = [(G.nodes[node]["y"], G.nodes[node]["x"]) for node in nodes]

    # Create Folium Map
    map_center = (locations[0][0], locations[0][1])
    m = folium.Map(location=map_center, zoom_start=14)

    # Add markers
    folium.Marker(location=map_center, popup="Depot (IAH Airport)", icon=folium.Icon(color="red")).add_to(m)
    
    for loc in locations:
        folium.Marker(location=loc, icon=folium.Icon(color="blue")).add_to(m)

    return m, locations, G
