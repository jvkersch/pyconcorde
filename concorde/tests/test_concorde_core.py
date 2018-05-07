import os
import unittest

import numpy as np
import numpy.testing as nptest

from concorde._concorde import _CCutil_gettsplib, _CCtsp_solve_dat
from concorde.tests.data_utils import get_dataset_path, get_solution_data


class TestCCutil_gettsplib(unittest.TestCase):

    def test_get_file_exists(self):
        # Given
        fname = get_dataset_path('berlin52')

        # When
        ncount, datagroup = _CCutil_gettsplib(fname)

        # Then
        self.assertEqual(ncount, 52)
        self.assertIsNotNone(datagroup)

    def test_get_file_does_not_exist(self):
        # Given
        fname = "no_such.tsp"

        # When
        ncount, datagroup = _CCutil_gettsplib(fname)

        # Then
        self.assertEqual(ncount, -1)
        self.assertIsNone(datagroup)


class TestCCtsp_solve_dat(unittest.TestCase):

    def test_solve_berlin_normal(self):
        # Given
        fname = get_dataset_path('berlin52')
        expected_tour, expected_opt_value = get_solution_data('berlin52')
        ncount, datagroup = _CCutil_gettsplib(fname)

        # When
        tour, val, success, foundtour, timebound = \
            _CCtsp_solve_dat(ncount, datagroup, "berlin", 0, 0)

        # Then
        nptest.assert_array_equal(tour, expected_tour)
        self.assertAlmostEqual(val, expected_opt_value)
        self.assertTrue(success)
        self.assertTrue(foundtour)
        # self.assertTrue(timebound)

    # def test_solve_berlin_timeout(self):
    #     # Given
    #     fname = os.path.join(BASEDIR, "data", "berlin52.tsp")
    #     ncount, datagroup = _CCutil_gettsplib(fname)

    #     # When
    #     tour, val, success, foundtour, timebound = \
    #         _CCtsp_solve_dat(ncount, datagroup, "berlin", 1e-10, 0)

    #     # Then
    #     self.assertTrue(success)
    #     self.assertFalse(timebound)
