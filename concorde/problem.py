from dataclasses import dataclass

import numpy as np
import tsplib95


@dataclass
class Problem:
    # The underlying tsplib95 problem instance
    _problem: object

    @classmethod
    def from_tsp_file(cls, fname):
        """Read in a TSP problem from a file in ``.tsp`` format."""
        problem = tsplib95.load(fname)
        return cls(_problem=problem)

    @classmethod
    def from_tsp_problem(cls, problem):
        """Initialize a TSP problem from a tsplib95 problem instance."""
        return cls(_problem=problem)

    @classmethod
    def from_coordinates(cls, xs, ys, norm="EUC_2D"):
        """Initialize a TSP problem from a list of coordinates."""
        coords = {i: (x, y) for (i, (x, y)) in enumerate(zip(xs, ys))}
        problem = tsplib95.models.StandardProblem(
            dimension=len(coords),
            edge_weight_type=norm,
            node_coords=coords,
        )
        return cls(_problem=problem)

    @classmethod
    def from_matrix(cls, matrix):
        """Initialize a TSP problem from a distance matrix."""
        matrix = np.asarray(matrix)
        problem = tsplib95.models.StandardProblem(
            dimension=matrix.shape[0],
            edge_weights=matrix.tolist(),
            edge_weight_type="EXPLICIT",
            edge_weight_format="FULL_MATRIX",
        )
        return cls(_problem=problem)

    @property
    def nodes(self):
        """Return nodes of the TSP problem."""
        if self._problem is None:
            return []
        return list(self._problem.get_nodes())

    def to_tsp(self, fname):
        """Write out TSP problem as a ``.tsp`` file."""
        with open(fname, "wt") as fp:
            self._problem.write(fp)
