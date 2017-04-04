import os
import unittest

import numpy as np
import numpy.testing as nptest

from pytsp._concorde import _CCutil_gettsplib, _CCtsp_solve_dat


BASEDIR = os.path.dirname(__file__)

BERLIN_TOUR = np.array(
    [0, 48, 31, 44, 18, 40,  7,  8,  9, 42, 32, 50, 10, 51, 13, 12, 46,
     25, 26, 27, 11, 24,  3,  5, 14,  4, 23, 47, 37, 36, 39, 38, 35, 34,
     33, 43, 45, 15, 28, 49, 19, 22, 29,  1,  6, 41, 20, 16,  2, 17, 30,
     21])


class TestCCutil_gettsplib(unittest.TestCase):

    def test_get_file_exists(self):
        # Given
        fname = os.path.join(BASEDIR, "data", "berlin52.tsp")

        # When
        ncount, datagroup = _CCutil_gettsplib(fname)

        # Then
        self.assertEqual(ncount, 52)
        self.assertIsNotNone(datagroup)

    def test_get_file_does_not_exist(self):
        # Given
        fname = os.path.join(BASEDIR, "data", "no_such.tsp")

        # When
        ncount, datagroup = _CCutil_gettsplib(fname)

        # Then
        self.assertEqual(ncount, -1)
        self.assertIsNone(datagroup)


class TestCCtsp_solve_dat(unittest.TestCase):

    def test_solve_berlin_normal(self):
        # Given
        fname = os.path.join(BASEDIR, "data", "berlin52.tsp")
        ncount, datagroup = _CCutil_gettsplib(fname)

        # When
        tour, val, success, foundtour, timebound = \
            _CCtsp_solve_dat(ncount, datagroup, "berlin", 0, 0)

        # Then
        nptest.assert_array_equal(tour, BERLIN_TOUR)
        self.assertAlmostEqual(val, 7542.0)
        self.assertTrue(success)
        self.assertTrue(foundtour)
        self.assertTrue(timebound)

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
