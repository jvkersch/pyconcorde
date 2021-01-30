from dataclasses import dataclass
from typing import List


@dataclass
class Solution:

    tour: List[int]

    @classmethod
    def from_file(cls, fname):
        with open(fname) as fp:
            _, tour = _read_sol_file(fp)
        return cls(tour=tour)

    def __str__(self):
        return f"Tour on {len(self.tour)} nodes"


def _read_sol_file(fp):
    n_nodes = int(next(fp))
    nodes = []
    for line in fp:
        nodes.extend(int(n) for n in line.split())
    return n_nodes, nodes
