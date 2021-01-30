from io import StringIO
import os
import textwrap
import unittest

from concorde.testing import temp_folder
from ..solution import Solution, _read_sol_file


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
    @temp_folder
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
