# import matplotlib.pyplot as plt
import copy
import time
from comtrade import Comtrade
import os

from util import convert_data_to_csv_style, filter_files, get_filename_keyword, get_filename_keyword_with_pole, get_max, print_log, save_to_csv, transform
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
    def _get_analog_from_file(字段, 量, Child="Child0", get_filename_keyword=get_filename_keyword):
        data_list = []
        for i in 字段:
            files = filter_files(filepath, [get_filename_keyword(i), Child])
            if len(files) <= 0:
                print_log("cannot find {}".format(i))
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
    print_log("读取直流场电流模拟量", 0.25)
    直流场电流 = func_get_analog_from_file(直流场电流模拟量_字段名, 直流场电流模拟量)
    print_log("读取直流场电压模拟量", 0.5)
    直流场电压 = func_get_analog_from_file(直流场电压模拟量_字段名, 直流场电压模拟量)
    直流场电压_PCP_CCP = func_get_analog_from_file(直流场电压模拟量_PCP_CCP_字段名, 直流场电压模拟量_PCP_CCP)
    print_log("读取换流变模拟量", 0.75)
    换流变 = func_get_analog_from_file(换流变模拟量_字段名, 换流变模拟量, Child="Child2")

    print_log("开始保存为CSV", 0.99)

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
    print_log("完成", 1)

def filter_all_analog(字段,总量):
    filtered_analog_quantity = []
    for per_field in 字段:
        per_field_quantity = []
        for per_quantity in 总量:
            if per_field in per_quantity["From"]:
                per_field_quantity.append(per_quantity)
        filtered_analog_quantity.append({
            "field": per_field,
            "quantity": per_field_quantity
        })
    return filtered_analog_quantity

def build_index(data):
    index = {}
    for d in data:
        for name in d["data_names"]:
            index[name] = d["display_name"]
    return index

def filter_analog_data(字段,总量):
    all_children = set([d["Child"] for d in 总量])
    Child_with_quantity = []
    for child in all_children:
        filtered_data = [d for d in 总量 if d["Child"] == child and 字段 in d["From"]]
        if len(filtered_data) > 0:
            Child_with_quantity.append({
                "Child": child,
                "data": filtered_data
            })
        print(f"Child: {child}, Filtered Data: {filtered_data}")
    return Child_with_quantity

def build_index_with_field(字段,总量):
    return build_index([d for d in 总量 if 字段 in d["From"]])

def get_DC_field_analog_quantity(filepath: str, csv_path: str):
    func_get_analog_from_file = get_analog_from_file(filepath)
    for per_field in 带极总字段:
        Child_with_quantity = filter_analog_data(per_field, 直流场总模拟量)
        index_with_field = build_index_with_field(per_field, 直流场总模拟量)
        analog_list = []

        for i in Child_with_quantity:
            quantity_index = build_index(i["data"])
            analog_list.extend(func_get_analog_from_file(per_field, quantity_index.keys(), Child=i["Child"], get_filename_keyword=get_filename_keyword_with_pole))

        fixed_analog_list = []

        for analog in analog_list:
            tmp = copy.deepcopy(analog)
            tmp["row"] = index_with_field[analog["row"]]
            fixed_analog_list.append(tmp)



if __name__ == '__main__':
    from pywebio.output import put_progressbar
    # find_diagram(r"C:\WorkSpace\Recoder\20231006test", r"C:\tmp\text.csv")
    put_progressbar("Progress", 0, "进度")