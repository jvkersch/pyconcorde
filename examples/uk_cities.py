# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import routingpy as rp
import folium
import webbrowser
import os

from concorde.problem import Problem
from concorde.concorde import Concorde

# Source for UK city data: ChatGPT

# Import city data
uk_cities = pd.read_csv('uk_cities.csv').sort_values('Population', ascending=False)

names = list(uk_cities['City'])
points = list(zip(uk_cities['Longitude'], uk_cities['Latitude']))

# Get asymmetric driving durations matrix
api_key = os.environ['ORS_API_KEY'] # Obtain free API key from https://openrouteservice.org/
api = rp.ORS(api_key=api_key)
matrix = api.matrix(locations=points, profile='driving-car')
m = np.matrix(matrix.durations)
m = m.astype(int) # Concorde solver requires integer matrix

# Instantiate problem and solver
problem = Problem.from_matrix(m)
solver = Concorde()

# Find tour
tour_data = solver.solve(problem)
solution = uk_cities.iloc[tour_data.tour]
print("Optimal tour:")
print(
    " -> ".join("{r.City}".format(r=row) for _, row in solution.iterrows())
)

# Obtain complete driving directions for the ordered loop
points_ordered = [points[i] for i in tour_data.tour]
points_ordered_return = points_ordered + [points_ordered[0]]
names_ordered = [names[i] for i in tour_data.tour]
directions = api.directions(locations=points_ordered_return, profile='driving-car')

# Visualize tour on map
def generate_map(coordinates, names, directions):

    # folium needs lat, long
    coordinates = [(y, x) for (x, y) in coordinates]
    route_points = [(y, x) for (x, y) in directions.geometry]
    lat_centre = np.mean([x for (x, y) in coordinates])
    lon_centre = np.mean([y for (x, y) in coordinates])
    centre = lat_centre, lon_centre

    m = folium.Map(location=centre, zoom_start=1, zoom_control=False)

    # plot the route line
    folium.PolyLine(route_points, color='red', weight=2).add_to(m)
    
    # plot each point with a hover tooltip  
    for i, (point, name) in enumerate(zip(coordinates, names)):
        folium.CircleMarker(location=point,
                      tooltip=f'{i}: {name}',
                      radius=2).add_to(m)

    custom_tile_layer = folium.TileLayer(
        tiles='http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
        attr='CartoDB Positron',
        name='Positron',
        overlay=True,
        control=True,
        opacity=0.7  # Adjust opacity to control the level of greying out
    )

    custom_tile_layer.add_to(m)
    folium.LayerControl().add_to(m)

    sw = (np.min([x for (x, y) in coordinates]), np.min([y for (x, y) in coordinates]))
    ne = (np.max([x for (x, y) in coordinates]), np.max([y for (x, y) in coordinates]))
    m.fit_bounds([sw, ne])

    return m

uk_cities_map = generate_map(points_ordered, names_ordered, directions)

# Save map HTML
uk_cities_map.save('uk_cities.html')

# Open the HTML file in a web browser
webbrowser.open('uk_cities.html')