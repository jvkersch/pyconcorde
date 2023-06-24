import os
import shutil
import tempfile
import textwrap
import unittest

import numpy as np

from concorde.testing import get_dataset_path
from ..problem import Problem


class TestConstructProblem(unittest.TestCase):
    def test_from_tsp_file(self):
        # Given
        tsp_fname = get_dataset_path("ch150.tsp")

        # When
        problem = Problem.from_tsp_file(tsp_fname)

        # Then
        self.assertEqual(problem.nodes, list(range(1, 151)))

    def test_from_matrix(self):
        # Given
        matrix = np.array([[0, 1, 2], [1, 0, 3], [2, 3, 0]])

        # When
        problem = Problem.from_matrix(matrix)

        # Then
        self.assertEqual(problem.nodes, [0, 1, 2])

    def test_from_coordinates(self):
        # Given
        xs = [1, 2, 3]
        ys = [4, 5, 6]

        # When
        problem = Problem.from_coordinates(xs, ys)

        # Then
        self.assertEqual(problem.nodes, [0, 1, 2])


class TestSaveProblem(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d)

    def test_matrix_to_tsp(self):
        # Given
        matrix = np.array([[0, 1, 2], [1, 0, 3], [2, 3, 0]])
        problem = Problem.from_matrix(matrix)
        fname = os.path.join(self.d, "problem.tsp")

        # When
        problem.to_tsp(fname)

        # Then
        self._assertContentsEqual(
            fname,
            textwrap.dedent(
                """\
            DIMENSION: 3
            EDGE_WEIGHT_TYPE: EXPLICIT
            EDGE_WEIGHT_FORMAT: FULL_MATRIX
            EDGE_WEIGHT_SECTION:
            0 1 2
            1 0 3
            2 3 0
            EOF"""
            ),
        )

    def test_coords_to_tsp(self):
        # Given
        xs = [3, 4, 5]
        ys = [7, 8, 9]
        problem = Problem.from_coordinates(xs, ys)
        fname = os.path.join(self.d, "problem.tsp")

        # When
        problem.to_tsp(fname)

        # Then
        self._assertContentsEqual(
            fname,
            textwrap.dedent(
                """\
            DIMENSION: 3
            EDGE_WEIGHT_TYPE: EUC_2D
            NODE_COORD_SECTION:
            0 3 7
            1 4 8
            2 5 9
            EOF"""
            ),
        )

    def _assertContentsEqual(self, path, expected):
        with open(path) as fp:
            self.assertEqual(fp.read(), expected)
