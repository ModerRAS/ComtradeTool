# import matplotlib.pyplot as plt
import copy
import time
from comtrade import Comtrade
import os
import numpy as np
from scipy.fft import fft, fftfreq

from util import convert_data_to_csv_style, filter_files, get_filename_keyword, get_filename_keyword_with_pole, get_max, print_log, save_to_csv, transform
from data import *

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

def get_analog_raw(rec: Comtrade, use_analog_list: list[str]):
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
        output_analog.append({
            "name": use_analog["name"],
            "value": rec.analog[use_analog["id"]]
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

def calculate_harmonic(voltage, harmonic_order, base_frequency=50, sampling_rate=1000):
    """
    计算指定次谐波的有效值

    参数：
    voltage: 电压数组，可以是 numpy 数组或普通数组
    harmonic_order: 谐波次数，如2表示二次谐波，3表示三次谐波，以此类推
    base_frequency: 基本频率，默认为50Hz
    sampling_rate: 采样率，默认为1000Hz
    as_numpy: 是否将输入转换为 numpy 数组，默认为 True

    返回值：
    harmonic_rms: 指定次谐波的有效值
    """

    if isinstance(voltage, np.ndarray):
        voltage_np = voltage  # 输入为 numpy 数组
    else:
        voltage_np = np.array(voltage)  # 将输入的电压数组转换为 numpy 数组

    # 傅立叶变换
    fft_values = fft(voltage_np)
    freqs = fftfreq(len(fft_values), 1/sampling_rate)

    # 找到指定次谐波频率的索引
    harmonic_freq = harmonic_order * base_frequency
    harmonic_idx = np.argmin(np.abs(freqs - harmonic_freq))

    # 计算指定次谐波的幅值
    harmonic_amplitude = np.abs(fft_values[harmonic_idx])

    # 计算指定次谐波的幅值密度
    amplitude_density = harmonic_amplitude / (len(fft_values) // 2)

    # 计算指定次谐波的有效值
    harmonic_rms = amplitude_density / np.sqrt(2)

    return harmonic_rms

def chunk_array(arr, chunk_size=1000):
    """
    将数组按照每 chunk_size 个元素切割成若干个子数组

    参数：
    arr: 输入的数组
    chunk_size: 每个子数组的大小，默认为1000

    返回值：
    chunks: 切割后的子数组列表
    """
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]
    return chunks

def overlap_chunks(arr, chunk_size=1000):
    """
    将数组按照重叠的方式切割成子数组

    参数：
    arr: 输入的数组
    chunk_size: 每个子数组的大小，默认为1000

    返回值：
    chunks: 切割后的子数组列表
    """
    chunks = [arr[i:i + chunk_size] for i in range(len(arr) - chunk_size + 1)]
    return chunks

if __name__ == '__main__':
    from pywebio.output import put_progressbar
    # find_diagram(r"C:\WorkSpace\Recoder\20231006test", r"C:\tmp\text.csv")
    put_progressbar("Progress", 0, "进度")
    get_DC_field_analog_quantity(r"C:\WorkSpace\Recoder\20231006test", r"C:\tmp\text4.csv")