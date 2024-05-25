import base64
import math
import os
import pickle
from comtrade import Comtrade
import numpy as np
from scipy.fftpack import fft, fftfreq

from util import filter_files, get_max, overlap_chunks, transform

from xmlrpc.server import SimpleXMLRPCServer

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
            "value": max_value,
            "frequency": rec.frequency,
            "time": rec.trigger_timestamp,
            "sample_rates": rec.cfg.sample_rates
        })
        # print(max([abs(), abs(min(analog))]))
    return output_analog
def get_analog_path_without_extension(name, path_without_extension: str, use_analog_list: list[str]):
    rec = load_diagram(path_without_extension)
    return {
            "name": name,
            "data": get_analog(rec, use_analog_list),
            "row": use_analog_list
        }

def get_analog_raw(filepath: str, use_analog_list: list[str]):
    rec = load_diagram(filepath)
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
            "value": rec.analog[use_analog["id"]],
            "frequency": rec.frequency,
            "time": rec.trigger_timestamp,
            "sample_rates": rec.cfg.sample_rates
        })
        # print(max([abs(), abs(min(analog))]))
    return base64.b64encode(pickle.dumps(output_analog)).decode('utf-8')


def get_all_analog_raw(filepath: str):
    rec = load_diagram(filepath)
    analog_list = []
    # 模拟通道的数量
    analog_count = rec.analog_count
    # 循环获取模拟通道的名称
    for i in range(analog_count):
        chan = rec.analog_channel_ids[i]
        analog_list.append({
                "name": chan,
                "id": i
                })
            
    output_analog = []
    # 循环输出81个模拟量通道的采集数据
    for use_analog in analog_list:
        output_analog.append({
            "name": use_analog["name"],
            "value": rec.analog[use_analog["id"]],
            "frequency": rec.frequency,
            "time": rec.trigger_timestamp,
            "sample_rates": rec.cfg.sample_rates
        })
        # print(max([abs(), abs(min(analog))]))
    return output_analog

def calculate_harmonic_rpc(voltage, harmonic_order, xx = 0, cyc_sample=100):
    return calculate_harmonic(pickle.loads(base64.b64decode(voltage)), harmonic_order, xx, cyc_sample)

def calculate_harmonic(voltage, harmonic_order, xx = 0, cyc_sample=100):
    """
    计算指定次谐波的有效值

    参数：
    voltage: 电压数组，普通数组
    harmonic_order: 谐波次数，如2表示二次谐波，3表示三次谐波，以此类推
    cyc_sample: 采样点数

    返回值：
    harmonic_rms: 指定次谐波的有效值
    """
    cyc_sample = int(cyc_sample)
    num10 = 0.0
    num11 = 0.0
    if (xx - (cyc_sample - 1)) < 0:
        xx = cyc_sample - 1
    for l in range(cyc_sample):
        num12 = voltage[xx - l]
        num10 += num12 * math.cos((float(harmonic_order) * -1.0 * float(l) * 2.0) * math.pi / cyc_sample)
        num11 += num12 * math.sin((float(harmonic_order) * -1.0 * float(l) * 2.0) * math.pi / cyc_sample)
    
    num10 = num10 * math.sqrt(2.0) / float(cyc_sample)
    num11 = num11 * math.sqrt(2.0) / float(cyc_sample)
    abs = math.sqrt(num10 * num10 + num11 * num11)
    deg = math.atan2(num10, num11) * 180.0 / math.pi
    return abs

def calculate_harmonic_fft(voltage, harmonic_order, base_frequency=50, sampling_rate=1000):
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


def get_max_harmonic(filepath: str, fft=False):
    """
    获得一个文件中所有模拟量的所有所需要的谐波在这一分钟内的最大值
    analog_harmonic:
    [{
      "name": analog_name, 
      "time": analog_time, 
      "total_harmonic": [{
        "harmonic_order": 1..10, 
        "harmonic": float
        }]
    }]
    """
    analogs = get_all_analog_raw(filepath=filepath)
    analog_harmonic = []
    for analog in analogs:
        total_harmonic = []
        cyc_sample = int(analog["sample_rates"][0][0] / analog["frequency"])
        for harmonic_order in range(1, 11):
            harmonic = []
            for xx in range(0, len(analog["value"]), cyc_sample):
                if fft:
                    harmonic.append(calculate_harmonic_fft(analog["value"], harmonic_order, analog["frequency"], analog["sample_rates"][0][0]))
                else:
                    harmonic.append(calculate_harmonic(analog["value"], harmonic_order, xx, cyc_sample))
            total_harmonic.append({
                "harmonic_order": harmonic_order,
                "harmonic": max(harmonic)
            })
        analog_harmonic.append({
            "name": analog["name"],
            "time": analog["time"],
            "total_harmonic": total_harmonic,
        })
    return analog_harmonic

def get_max_harmonic_rpc(filepath: str, fft=False):
    return base64.b64encode(pickle.dumps(get_max_harmonic(filepath, fft))).decode("utf-8")
        

if __name__ == '__main__':
    server = SimpleXMLRPCServer(('0.0.0.0', 4242))
    server.register_function(get_analog_path_without_extension, 'get_analog_path_without_extension')
    server.register_function(get_analog_raw, 'get_analog_raw')
    server.register_function(calculate_harmonic_rpc, 'calculate_harmonic')
    server.register_function(get_max_harmonic_rpc, 'get_max_harmonic')
    server.serve_forever()