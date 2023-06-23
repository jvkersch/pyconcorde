from io import StringIO
import os
import textwrap
import unittest

from concorde.testing import temp_folder
from ..solution import Solution, _read_sol_file

OUTPUT = """\
Host: laundry-4.local  Current process id: 56795
Using random seed 1687525406
Problem Name: ch150
Problem Type: TSP
150 city Problem (churritz)
Number of Nodes: 150
Rounded Euclidean Norm (CC_EUCLIDEAN)
Set initial upperbound to 6528 (from tour)
  LP Value  1: 6374.000000  (0.01 seconds)
  LP Value  2: 6460.000000  (0.01 seconds)
  LP Value  3: 6512.250000  (0.03 seconds)
  LP Value  4: 6520.015960  (0.04 seconds)
  LP Value  5: 6522.000000  (0.06 seconds)
  LP Value  6: 6523.528455  (0.07 seconds)
  LP Value  7: 6525.292683  (0.09 seconds)
  LP Value  8: 6526.434211  (0.14 seconds)
  LP Value  9: 6528.000000  (0.14 seconds)
New lower bound: 6528.000000
Final lower bound 6528.000000, upper bound 6528.000000
Exact lower bound: 6528.000000
DIFF: 0.000000
Final LP has 231 rows, 367 columns, 2234 nonzeros
Optimal Solution: 6528.00
Number of bbnodes: 1
Total Running Time: 0.21 (seconds)
"""


class TestReadSolFile(unittest.TestCase):
    def test_read_sol_file(self):
        # Given
        data = textwrap.dedent(
            """\
            5
            0 4
            3 2 1"""
        )

        # When
        n, nodes = _read_sol_file(StringIO(data))

        # Then
        self.assertEqual(n, 5)
        self.assertEqual(nodes, [0, 4, 3, 2, 1])


class TestSolution(unittest.TestCase):
    @temp_folder()
    def test_from_file(self, d):
        # Given
        data = textwrap.dedent(
            """\
            5
            0 4
            3 2 1"""
        )
        fname = os.path.join(d, "tour.sol")
        with open(fname, "wt") as fp:
            fp.write(data)

        # When
        solution = Solution.from_file(fname)

        # Then
        self.assertEqual(solution.tour, [0, 4, 3, 2, 1])

    def test_optimal_value(self):
        # Given
        solution = Solution(tour=[], output=OUTPUT)

        # When/then
        self.assertEqual(solution.optimal_value, 6528.0)

    def test_running_time(self):
        # Given
        solution = Solution(tour=[], output=OUTPUT)

        # When/then
        self.assertEqual(solution.running_time, 0.21)
