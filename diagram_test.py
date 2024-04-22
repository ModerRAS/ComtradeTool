import csv
import time
import unittest

from analog_rpc_client import get_analog_raw
from diagram import calculate_harmonic, find_diagram

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
    def test_calculate_harmonic(self):
        analog = get_analog_raw("testdata/04时54分09秒/2024年03月25日04时54分09秒", ["822B极Ⅱ低端换流变交流系统A相电压Uac_L1"])[0]
        correct_answer = [0.1545852721927649, 0.0004513942720173336, 0.005483978563828073, 0.0011817627160931419, 0.001099846773165423]
        start_time = time.time()
        for xiebo in range(1, 6):
            compute_answer = calculate_harmonic(analog["value"], xiebo, 0, 20)
            print("{}次谐波含量为{}".format(xiebo, compute_answer))
            self.assertTrue(abs(compute_answer - correct_answer[xiebo - 1]) < 1e-5)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"计算所需的时间：{elapsed_time} 秒")