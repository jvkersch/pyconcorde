import unittest
import warnings

import numpy.testing as nptest

from concorde.tsp import TSPSolver
from concorde.tests.data_utils import get_dataset_path, get_solution_data


class TestTSPSolver(unittest.TestCase):
    def test_from_data(self):
        # Given
        xs = [1, 2, 3]
        ys = [4, 5, 6]
        name = "testdataset"
        norm = "EUC_2D"

        # When
        datagroup = TSPSolver.from_data(xs, ys, norm, name)

        # Then
        self.assertIsNotNone(datagroup._data)
        self.assertEqual(datagroup._ncount, 3)
        nptest.assert_allclose(datagroup.x, xs)
        nptest.assert_allclose(datagroup.y, ys)

    def test_from_data_warns_small_coordinates(self):
        # Coordinates in [0, 1] get truncated to 0 by Concorde
        xs = [0.1, 0.5, 0.9]
        ys = [0.2, 0.6, 0.8]
        with self.assertWarns(UserWarning) as ctx:
            TSPSolver.from_data(xs, ys, "EUC_2D")
        self.assertIn("[-1, 1]", str(ctx.warning))

    def test_from_data_warns_large_coordinates(self):
        # Large coordinates risk integer overflow in Concorde
        xs = [1e8, 2e8, 3e8]
        ys = [4e8, 5e8, 6e8]
        with self.assertWarns(UserWarning) as ctx:
            TSPSolver.from_data(xs, ys, "EUC_2D")
        self.assertIn("1e7", str(ctx.warning))

    def test_from_data_no_warning_normal_coordinates(self):
        # Normal coordinates should not trigger any warning
        xs = [100, 200, 300]
        ys = [400, 500, 600]
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            TSPSolver.from_data(xs, ys, "EUC_2D")

    def test_solve(self):
        # Given
        fname = get_dataset_path("berlin52")
        expected_tour, expected_opt_value = get_solution_data("berlin52")
        datagroup = TSPSolver.from_tspfile(fname)

        # When
        tour, val, success, foundtour, hit_timebound = datagroup.solve()

        # Then
        nptest.assert_array_equal(tour, expected_tour)
        self.assertAlmostEqual(val, expected_opt_value)
        self.assertTrue(success)
        self.assertTrue(foundtour)
        self.assertFalse(hit_timebound)
