
import csv
import time
import os

from analog_rpc_client import get_analog_path_without_extension, get_max_harmonic
from util import convert_data_to_csv_style, filter_files, get_filename_keyword, get_filename_keyword_with_pole, parallel_process, remove_all_extensions, save_to_csv
from data import *
from log import print_log

def get_analog_from_file(filepath):
    def _get_analog_from_file(字段, 量, Child="Child0", get_filename_keyword=get_filename_keyword):
        data_list = []
        for i in 字段:
            files = filter_files(filepath, [get_filename_keyword(i), Child])
            if len(files) <= 0:
                print_log("cannot find {}".format(i))
                continue
            path_without_extension, extension = os.path.splitext(files[0])
            analog_tmp = get_analog_path_without_extension(i, path_without_extension, 量)
            data_list.append(analog_tmp)
        return data_list

    return _get_analog_from_file


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

def find_diagram(filepath: str, csv_path: str):
    start_time = time.time()
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

def find_diagram_hlb2(filepath: str, csv_path: str):
    start_time = time.time()
    # 直流场电流模拟量
    func_get_analog_from_file = get_analog_from_file(filepath)
    print_log("读取换流变2模拟量", 0.5)
    换流变2 = func_get_analog_from_file(换流变2字段, 换流变2模拟量, Child="Child2")

    print_log("开始保存为CSV", 0.99)

    data_list = [
        convert_data_to_csv_style("换流变2", 换流变2),
    ]
    save_to_csv(data_list, csv_path)
    end_time = time.time()
    # 计算时间差
    elapsed_time = end_time - start_time
    print(f"程序运行时间为：{elapsed_time} 秒")
    print_log("完成", 1)

def get_analog_quantity(filepath: str, csv_path: str):
    def _get_analog_quantity(字段, 量, 量名称):
        func_get_analog_from_file = get_analog_from_file(filepath)
        analog_data_list = []
        for iter, per_field in enumerate(字段):
            print_log("开始读取{}".format(per_field), progress=float(iter)/len(字段))
            Child_with_quantity = filter_analog_data(per_field, 量)
            index_with_field = build_index_with_field(per_field, 量)
            rows_list = [i["display_name"] for i in 量]
            analog_list = []

            for i in Child_with_quantity:
                quantity_index = build_index(i["data"])
                analog_list.extend(func_get_analog_from_file([per_field, ], quantity_index.keys(), Child=i["Child"], get_filename_keyword=get_filename_keyword_with_pole))
    
            quantity_data = []
    
            for analog in analog_list:
                for quantity in analog["data"]:
                    quantity_data.append({
                        "name": index_with_field[quantity["name"]],
                        "value": quantity["value"]
                    })
            analog_data_list.append({
                "name": per_field,
                "data": quantity_data,
                "row": rows_list
            })
        data_list = convert_data_to_csv_style(量名称, analog_data_list, transpose=False)
        data_list["rows"] = [{"name": i["display_name"]} for i in 量]
        save_to_csv([data_list, ], csv_path)
        print_log("完成", progress=1)
    return _get_analog_quantity



def get_DC_field_analog_quantity(filepath: str, csv_path: str):
    get_analog_quantity(filepath, csv_path)(带极总字段, 直流场总模拟量, "直流场模拟量")

def get_hlb1_analog_quantity(filepath: str, csv_path: str):
    get_analog_quantity(filepath, csv_path)(换流变1字段, 换流变1总模拟量, "换流变1总模拟量")

def get_all_harmonic(filepath: str):
    """
    all_harmonic:
    [{"name": path_without_extension, "harmonic": get_max_harmonic(path_without_extension)}]
    """
    all_files = filter_files(filepath, ".cfg")
    all_files = set(map(remove_all_extensions, all_files))
    def _process_file(path_without_extension):
        # path_without_extension = remove_all_extensions(file)
        per_file_harmonic = get_max_harmonic(path_without_extension)
        return {
            "name": path_without_extension,
            "harmonic": per_file_harmonic
        }
    all_harmonic = parallel_process(_process_file, all_files, print_log)
    return all_harmonic



def generate_all_harmonic_list(all_harmonic: list):
    """
    export object type:
    [[fmttime, wave_name, harmonic_order, harmonic], ]
    """
    all_harmonic_list = []
    harmonic_count = len(all_harmonic)
    for index, harmonic in enumerate(all_harmonic):
        # get harmonic
        harmonic_data = harmonic["harmonic"]
        for per_harmonic_data in harmonic_data:
            name = per_harmonic_data["name"]
            harmonic_time = per_harmonic_data["time"].strftime("%Y-%m-%d %H:%M:%S")
            for harmonic_index in per_harmonic_data["total_harmonic"]:
                harmonic_order = harmonic_index["harmonic_order"]
                harmonic_value = harmonic_index["harmonic"]
                all_harmonic_list.append([
                    harmonic_time,
                    name,
                    harmonic_order,
                    harmonic_value
                ])
        
    return all_harmonic_list

def generate_all_harmonic_list_csv(filepath: str, csv_path: str):
    """
    export object type:
    [[fmttime, wave_name, harmonic_order, harmonic], ]
    """
    all_harmonic = get_all_harmonic(filepath)
    all_harmonic_list = generate_all_harmonic_list(all_harmonic)
    # 按照列表文件生成csv
    with open(csv_path, "w", encoding='gbk', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["时间", "波形名称", "谐波次数", "谐波值"])
        writer.writerows(all_harmonic_list)
    print_log("完成", progress=1)

if __name__ == '__main__':
    start_time = time.time()
    print(generate_all_harmonic_list_csv("testdata/04时54分09秒", "testdata/04时54分09秒.csv"))
    end_time = time.time()
    print(end_time - start_time)