from dataclasses import dataclass
import re
from typing import List


@dataclass
class Solution:
    """Concorde TSP solution."""

    tour: List[int]

    output: str

    @classmethod
    def from_file(cls, fname, output=""):
        """Create a solution from a Concorde ``.sol`` file.

        Parameters
        ----------
        fname : str
            Path of the ``.sol`` file.
        output : str
            Output from the concorde run.

        """
        with open(fname) as fp:
            _, tour = _read_sol_file(fp)
        return cls(tour=tour, output=output)
  
    def __str__(self):
        """Create string representation of the tour."""
        return f"Tour on {len(self.tour)} nodes"
    
    def remove_ghost_nodes(self):
        """
            Remove ghost nodes (indices n, n+1, ..., 2n-1 of matrix) from solution tour of asymmetric problem.
            Given an asymmetric problem on n nodes, solution.tour will take one of the following forms:
                1. [i1, i1 + n, i2, i2 + n, i3, i3 + n, ..., in, in + n ]
                2. [i1, i2 + n, i2, i3 + n, i3, ..., in + n, in, i1 + n ]
            In either case, the original nodes are those at even indices
        """
        self.tour = self.tour[::2]
 
    @property
    def optimal_value(self):
        """Return optimal tour value."""
        value = _extract_value(self.output, "Optimal Solution: ")
        return float(value)

    @property
    def running_time(self):
        """Return total running time (in seconds) to compute tour."""
        value = _extract_value(self.output, "Total Running Time: ")
        return float(value.split()[0])
    



def _read_sol_file(fp):
    n_nodes = int(next(fp))
    nodes = []
    for line in fp:
        nodes.extend(int(n) for n in line.split())
    return n_nodes, nodes


def _extract_value(s, key):
    m = re.search(f"{key}(.+)", s)
    if not m:
        raise RuntimeError(f"Key {key!r} not found in string {s!r}")
    return m.groups()[0]
