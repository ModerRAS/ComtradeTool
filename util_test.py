import unittest
from util import *

class TestUtil(unittest.TestCase):

    def test_get_max(self):
        self.assertEqual(get_max([-1, -2, -3, -4, -5]), -5)
        self.assertEqual(get_max([1, 2, 3, 4, 5]), 5)
        self.assertEqual(get_max([-1, -2, 3, 4, -5]), -5)
        self.assertEqual(get_max([1, -2, -3, 4, -5]), -5)
        self.assertEqual(get_max([1, 2, 3, -4, -5]), -5)