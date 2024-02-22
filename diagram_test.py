import unittest

from diagram import find_diagram

class TestDiagram(unittest.TestCase):

    def test_find_diagram(self):
        find_diagram("testdata/diagram1", "testdata/diagram1.csv")
        with open("testdata/diagram1.csv", 'rb') as f:
            data = f.read()
        with open("testdata/result1.csv", 'rb') as f:
            example_result = f.read()
        for i,d in enumerate(data):
            self.assertEqual(d, example_result[i])