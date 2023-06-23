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
