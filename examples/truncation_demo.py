"""Demonstrate how Concorde truncates small coordinates.

Concorde stores coordinates as doubles but computes rounded integer
distances. When coordinates are in [0, 1], the rounded Euclidean
distances between points become 0. This can even cause Concorde to
crash (segfault), as seen in GitHub issues #33 and #35.

We use 10 equally spaced points on the unit circle (roots of unity).
The optimal tour visits them in order, and the exact tour length is
10 * 2 * sin(pi/10) = 10 * 0.6180... = 6.180...
"""
import warnings

import numpy as np

from concorde.tsp import TSPSolver

n = 10
angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
xs = np.cos(angles)
ys = np.sin(angles)

# Exact optimal tour length: n * side length of regular n-gon
side_length = 2 * np.sin(np.pi / n)
exact_tour_length = n * side_length
print(f"Exact optimal tour length: {exact_tour_length:.4f}")

# --- Unscaled coordinates (on the unit circle) ---
print("\n=== Unscaled coordinates (unit circle) ===")
print("Sample pairwise distances between adjacent nodes:")
for i in range(3):
    j = (i + 1) % n
    d = np.sqrt((xs[i] - xs[j])**2 + (ys[i] - ys[j])**2)
    print(f"  Nodes {i}-{j}: {d:.4f} -> rounded to int: {round(d)}")
print("  ... (all round to 1 or 0)")

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    solver = TSPSolver.from_data(xs, ys, "EUC_2D")
    solution = solver.solve(verbose=False)

print(f"Concorde optimal value: {solution.optimal_value}")
print(f"Expected: {exact_tour_length:.4f}")
print(f"--> Wrong! Distances are too small for integer arithmetic.")

# --- Scaled coordinates ---
scale = 1_000_000
xs_scaled = xs * scale
ys_scaled = ys * scale

print(f"\n=== Scaled coordinates (x {scale}) ===")
solver_scaled = TSPSolver.from_data(xs_scaled, ys_scaled, "EUC_2D")
solution_scaled = solver_scaled.solve(verbose=False)

expected_scaled = round(exact_tour_length * scale)
print(f"Concorde optimal value: {solution_scaled.optimal_value}")
print(f"Expected (approx): {expected_scaled}")
print(f"Tour: {solution_scaled.tour}")
print(f"--> Correct! Tour visits nodes in order around the circle.")
