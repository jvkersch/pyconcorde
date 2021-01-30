import unittest

from concorde.testing import ConcordeTestMixin, get_dataset_path
from ..concorde import run_concorde
from ..problem import Problem


class TestRunConcorde(ConcordeTestMixin, unittest.TestCase):
    def test_run_on_problem(self):
        # Given
        problem = Problem.from_tsp_file(get_dataset_path("ch150.tsp"))

        # When
        solution = run_concorde(problem)

        # Then
        self.assertEqual(solution.tour, [0, 1, 2, 3, 4])
