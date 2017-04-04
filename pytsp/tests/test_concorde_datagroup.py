import unittest

import numpy.testing as nptest

from pytsp.tsp import ConcordeDataGroup


class TestConcordeDataGroup(unittest.TestCase):

    def test_from_data(self):
        # Given
        xs = [1, 2, 3]
        ys = [4, 5, 6]
        name = "testdataset"
        norm = "EUC_2D"

        # When
        datagroup = ConcordeDataGroup.from_data(xs, ys, norm, name)

        # Then
        self.assertIsNotNone(datagroup._data)
        self.assertEqual(datagroup._ncount, 3)
        nptest.assert_allclose(datagroup.x, xs)
        nptest.assert_allclose(datagroup.y, ys)
