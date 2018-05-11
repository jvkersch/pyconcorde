import unittest

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

    def test_solve(self):
        # Given
        fname = get_dataset_path('berlin52')
        expected_tour, expected_opt_value = get_solution_data('berlin52')
        datagroup = TSPSolver.from_tspfile(fname)

        # When
        tour, val, success, foundtour, hit_timebound = datagroup.solve()

        # Then
        nptest.assert_array_equal(tour, expected_tour)
        self.assertAlmostEqual(val, expected_opt_value)
        self.assertTrue(success)
        self.assertTrue(foundtour)
        self.assertFalse(hit_timebound)
