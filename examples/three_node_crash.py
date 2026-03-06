"""Demonstrate that Concorde crashes (segfault) with 3 nodes.

This is a bug in Concorde's internal LP/matching code, not a coordinate
scaling issue. The coordinates here are well-scaled integers, but
Concorde cannot handle the degenerate case of only 3 nodes.

With 4 or more nodes, the same kind of input works fine.
"""
from concorde.tsp import TSPSolver

# A simple triangle with well-scaled integer coordinates
xs = [0, 1000, 500]
ys = [0, 0, 866]

print("Solving TSP with 3 nodes (expect crash)...")
print(f"Coordinates: {list(zip(xs, ys))}")

solver = TSPSolver.from_data(xs, ys, "EUC_2D")
solution = solver.solve(verbose=False)

# This line is never reached
print(f"Tour: {solution.tour}")
