import unittest

import clpy
from clpy.core import core


class TestGetStridesForNocopyReshape(unittest.TestCase):

    def test_different_size(self):
        a = core.ndarray((2, 3))
        self.assertEqual(core._get_strides_for_nocopy_reshape(a, (1, 5)),
                         [])

    def test_one(self):
        a = core.ndarray((1,), dtype=clpy.int32)
        self.assertEqual(core._get_strides_for_nocopy_reshape(a, (1, 1, 1)),
                         [4, 4, 4])

    def test_normal(self):
        # TODO(nno): write test for normal case
        pass
