import csv
import unittest

from diagram import find_diagram

class TestDiagram(unittest.TestCase):
    def compare_csv(self, file1, file2):
        with open(file1, encoding='gbk', newline='') as f1, open(file2, encoding='gbk', newline='') as f2:
            reader1 = csv.reader(f1)
            reader2 = csv.reader(f2)
            for row1, row2 in zip(reader1, reader2):
                if row1 != row2:
                    print(row1, row2)
                    return False
            # Check if both files have the same number of rows
            return next(reader1, None) is None and next(reader2, None) is None
    def test_find_diagram(self):
        find_diagram("testdata/diagram1", "testdata/diagram1.csv")
        self.assertTrue(self.compare_csv("testdata/diagram1.csv", "testdata/result1.csv"))