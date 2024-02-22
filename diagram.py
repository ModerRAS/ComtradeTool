# import matplotlib.pyplot as plt
import json
import time
import chardet
from comtrade import Comtrade
import csv
import os
import codecs
from pywebio.output import *

from util import convert_data_to_csv_style, filter_files, get_filename_keyword, get_max, save_to_csv, transform
from data import *


log_list = []

def load_diagram(file_header: str):
    cfgFile = file_header + ".CFG"
    datFile = file_header + ".DAT"
    rec = Comtrade()
    try:
        rec.load(cfgFile, datFile)
    except UnicodeDecodeError as e:
        ocfgfile = cfgFile + "cfg"
        transform(cfgFile,ocfgfile)

        rec.load(ocfgfile, datFile)
    return rec


def get_analog(rec: Comtrade, use_analog_list: list[str]):
    analog_list = []
    # 模拟通道的数量
    analog_count = rec.analog_count
    # 循环获取模拟通道的名称
    for i in range(analog_count):
        chan = rec.analog_channel_ids[i]
        if chan in use_analog_list:
            analog_list.append({
                "name": chan,
                "id": i
            })
    output_analog = []
    # 循环输出81个模拟量通道的采集数据
    for use_analog in analog_list:
        max_value = get_max(rec.analog[use_analog["id"]])
        output_analog.append({
            "name": use_analog["name"],
            "value": max_value
        })
        # print(max([abs(), abs(min(analog))]))
    return output_analog


def get_analog_from_file(filepath):
    def _get_analog_from_file(字段, 量, Child="Child0"):
        data_list = []
        for i in 字段:
            # put_markdown("读取字段 {}".format(i))
            files = filter_files(filepath, [get_filename_keyword(i), Child])
            if len(files) <= 0:
                put_markdown("cannot find {}".format(i))
                continue
            path_without_extension, extension = os.path.splitext(files[0])
            rec = load_diagram(path_without_extension)
            data_list.append({
                "name": i,
                "data": get_analog(rec, 量),
                "row": 量
            })
        return data_list

    return _get_analog_from_file

def find_diagram(filepath: str, csv_path: str):
    start_time = time.time()
    log_list.clear()
    # 直流场电流模拟量
    func_get_analog_from_file = get_analog_from_file(filepath)
    put_markdown("读取直流场电流模拟量")
    直流场电流 = func_get_analog_from_file(直流场电流模拟量_字段名, 直流场电流模拟量)
    put_markdown("读取直流场电压模拟量")
    直流场电压 = func_get_analog_from_file(直流场电压模拟量_字段名, 直流场电压模拟量)
    直流场电压_PCP_CCP = func_get_analog_from_file(直流场电压模拟量_PCP_CCP_字段名, 直流场电压模拟量_PCP_CCP)
    put_markdown("读取换流变模拟量")
    换流变 = func_get_analog_from_file(换流变模拟量_字段名, 换流变模拟量, Child="Child2")

    put_markdown("开始保存为CSV")

    data_list = [
        convert_data_to_csv_style("直流场电流", 直流场电流),
        convert_data_to_csv_style("直流场电压", 直流场电压),
        convert_data_to_csv_style("直流场电压", 直流场电压_PCP_CCP),
        convert_data_to_csv_style("换流变", 换流变)
    ]
    save_to_csv(data_list, csv_path)
    end_time = time.time()
    # 计算时间差
    elapsed_time = end_time - start_time
    print(f"程序运行时间为：{elapsed_time} 秒")
    pass

if __name__ == '__main__':
    find_diagram(r"C:\WorkSpace\Recoder\20231006test", r"C:\tmp\text.csv")