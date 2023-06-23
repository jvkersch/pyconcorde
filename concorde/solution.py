from dataclasses import dataclass


@dataclass
class Solution:
    """Concorde TSP solution."""

    tour: list[int]

    @classmethod
    def from_file(cls, fname):
        """Create a solution from a Concorde ``.sol`` file.

        Parameters
        ----------
        fname : str
            Path of the ``.sol`` file.

        """
        with open(fname) as fp:
            _, tour = _read_sol_file(fp)
        return cls(tour=tour)

    def __str__(self):
        """Create string representation of the tour."""
        return f"Tour on {len(self.tour)} nodes"


def _read_sol_file(fp):
    n_nodes = int(next(fp))
    nodes = []
    for line in fp:
        nodes.extend(int(n) for n in line.split())
    return n_nodes, nodes
