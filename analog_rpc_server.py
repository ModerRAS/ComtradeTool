import base64
import math
import pickle
from comtrade import Comtrade

from util import get_max, overlap_chunks, transform

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



def get_max_harmonic(filepath: str):
    
    analogs = get_all_analog_raw(filepath=filepath)
    analog_harmonic = []
    for analog in analogs:
        total_harmonic = []
        cyc_sample = analog["sample_rates"][0][0] / analog["frequency"]
        for harmonic_order in range(1, 11):
            harmonic = []
            for xx in range(len(analog["value"])):
                harmonic.append(calculate_harmonic(analog["value"], harmonic_order, xx, cyc_sample))
            total_harmonic.append({
                "harmonic_order": harmonic_order,
                "harmonic": max(harmonic)
            })
        analog_harmonic.append({
            "name": analog["name"],
            "total_harmonic": total_harmonic,
        })
        
                

if __name__ == '__main__':
    server = SimpleXMLRPCServer(('0.0.0.0', 4242))
    server.register_function(get_analog_path_without_extension, 'get_analog_path_without_extension')
    server.register_function(get_analog_raw, 'get_analog_raw')
    server.register_function(calculate_harmonic_rpc, 'calculate_harmonic')
    server.serve_forever()