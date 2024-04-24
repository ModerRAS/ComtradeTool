import csv
from datetime import datetime
import time
import unittest

from analog_rpc_client import get_analog_raw
from diagram import find_diagram, generate_all_harmonic_list, generate_all_harmonic_list_csv, get_all_harmonic
from analog_rpc_client import calculate_harmonic

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
    def test_get_all_harmonic(self):
        start_time = time.time()
        print(get_all_harmonic("testdata/04时54分09秒"))
        end_time = time.time()
        print(end_time - start_time)
    def test_generate_all_harmonic_list(self):
        test_data = [
            {
                "name": "wavefile1",
                "harmonic": [{
                    "name": "wave1",
                    "time": datetime(2022, 1, 1, 10, 0, 0),
                    "total_harmonic": [
                        {"harmonic_order": 1, "harmonic": 100},
                        {"harmonic_order": 2, "harmonic": 200},
                    ],
                }, ]
            },
            {
                "name": "wavefile2",
                "harmonic": [{
                    "name": "wave2",
                    "time": datetime(2022, 1, 1, 11, 0, 0),
                    "total_harmonic": [
                        {"harmonic_order": 1, "harmonic": 300},
                        {"harmonic_order": 2, "harmonic": 400},
                    ],
                }, ]
            },
        ]
        result = generate_all_harmonic_list(test_data)
        self.assertEqual(result, [
            ["2022-01-01 10:00:00", "wave1", 1, 100],
            ["2022-01-01 10:00:00", "wave1", 2, 200],
            ["2022-01-01 11:00:00", "wave2", 1, 300],
            ["2022-01-01 11:00:00", "wave2", 2, 400],
        ])