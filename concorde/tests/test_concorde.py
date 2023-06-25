from subprocess import CalledProcessError
import unittest
from unittest.mock import patch

from concorde.testing import get_dataset_path
from ..concorde import Concorde, ConcordeError
from ..problem import Problem

TINY5_OUTPUT = """\
concorde tiny5.tsp
Host: laundry-4.local  Current process id: 89129
Using random seed 1687691239
Problem Name: tiny5
5-node test problem
Problem Type: TSP
Number of Nodes: 5
Rounded Euclidean Norm (CC_EUCLIDEAN)
Optimal Solution: 20.00
Total Running Time: 0.00 (seconds)
"""


class TestRunConcorde(unittest.TestCase):
    def test_run_on_problem(self):
        # Given
        problem = Problem.from_tsp_file(get_dataset_path("tiny5.tsp"))
        concorde = Concorde()

        # When
        solution = concorde.solve(problem)

        # Then
        self.assertEqual(solution.tour, [0, 4, 2, 3, 1])
        self.assertEqual(solution.optimal_value, 20)
        self.assertEqual(_tail(solution.output, 7), _tail(TINY5_OUTPUT, 7))

    @patch("concorde.concorde.subprocess.run")
    def test_run_on_problem_error(self, mock_subprocess_run):
        # Given
        problem = Problem.from_tsp_file(get_dataset_path("tiny5.tsp"))
        concorde = Concorde()
        mock_subprocess_run.side_effect = CalledProcessError(1, "foo")

        # When/then
        with self.assertRaises(ConcordeError):
            concorde.solve(problem)


def _tail(s, n):
    return "\n".join(s.splitlines()[-n:])
