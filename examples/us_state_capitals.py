# -*- coding: utf-8 -*-
from __future__ import division, print_function

import numpy as np
import pandas as pd

from concorde.tsp import TSPSolver

# Source for state capital data:
# http://www.jetpunk.com/data/countries/united-states/state-capitals-list

state_capitals = pd.read_table(
    "us_state_capitals.tsv", header=None,
    names=['state', 'city', 'lat', 'lon']
)

# Keep only the lower 48
state_capitals = state_capitals[
    (state_capitals.state != 'Alaska') & (state_capitals.state != 'Hawaii')]
state_capitals.reset_index(inplace=True, drop=True)

# Instantiate solver
solver = TSPSolver.from_data(
    state_capitals.lat,
    state_capitals.lon,
    norm="GEO"
)

# Find tour
tour_data = solver.solve()
assert tour_data.success

solution = state_capitals.iloc[tour_data.tour]
print("Optimal tour:")
print(u' -> '.join(
    '{r.city}, {r.state}'.format(r=row) for _, row in solution.iterrows()))

# Make a plot
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import shapely.geometry as sgeom

import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader

ax = plt.axes([0, 0, 1, 1], projection=ccrs.LambertConformal())
ax.set_extent([-125, -66.5, 20, 50], ccrs.Geodetic())

shapename = 'admin_1_states_provinces_lakes_shp'
states_shp = shpreader.natural_earth(resolution='110m',
                                     category='cultural', name=shapename)

ax.background_patch.set_visible(False)
ax.outline_patch.set_visible(False)

tour = sgeom.LineString(list(zip(solution.lon, solution.lat)))
capitals = sgeom.MultiPoint(list(zip(solution.lon, solution.lat)))

for state in shpreader.Reader(states_shp).geometries():
    facecolor = [0.9375, 0.9375, 0.859375]
    edgecolor = 'black'

    ax.add_geometries([state], ccrs.PlateCarree(),
                      facecolor=facecolor, edgecolor=edgecolor)

ax.add_geometries([tour], ccrs.PlateCarree(),
                  facecolor='none', edgecolor='red')
for lat, lon in zip(solution.lat, solution.lon):
    ax.plot(lon, lat, 'ro', transform=ccrs.PlateCarree())
    
plt.savefig("us_state_capitals.png", bbox_inches='tight')
plt.show()
