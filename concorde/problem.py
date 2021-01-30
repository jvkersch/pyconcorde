from dataclasses import dataclass

import numpy as np
import tsplib95


@dataclass
class Problem:

    # The underlying tsplib95 problem instance
    _problem: object

    @classmethod
    def from_tsp_file(cls, fname):
        problem = tsplib95.load(fname)
        return cls(_problem=problem)

    @classmethod
    def from_tsp_problem(cls, problem):
        return cls(_problem=problem)

    @classmethod
    def from_coordinates(cls, xs, ys, norm="EUC_2D"):
        coords = {i: (x, y) for (i, (x, y)) in enumerate(zip(xs, ys))}
        problem = tsplib95.models.StandardProblem(
            dimension=len(coords), edge_weight_type=norm, node_coords=coords,
        )
        return cls(_problem=problem)

    @classmethod
    def from_matrix(cls, matrix):
        # Assemble TSP problem from distance matrix
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
        if self._problem is None:
            return []
        return list(self._problem.get_nodes())

    def to_tsp(self, fname):
        with open(fname, "wt") as fp:
            self._problem.write(fp)
