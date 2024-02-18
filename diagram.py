# import matplotlib.pyplot as plt
from comtrade import Comtrade
import csv
import os

直流场电流模拟量 = [
    "IDEL1",
    "IDEL2",
    "IDEE1",
    "IDEE2",
    "IDGND",
    "IDME",
    "INBGS",
    "IMRTB",
    "IGRTS",
    "IANE",
    "ICN",
    "IAN",
    "IZT1",
    "IZ1T2",
    "IZ2T2",
]

直流场电流模拟量_字段名 = [
    "PPR1A",
    "PPR1B",
    "PPR1C",
    "PPR2A",
    "PPR2B",
    "PPR2C"
]


# CPR/CCP/PCP
直流场电压模拟量 = [
    "UDL",
    "UDM",
    "UDN"
]

直流场电压模拟量_字段名 = [
    "CPR11A",
    "CPR11B",
    "CPR11C",
    "CPR12A",
    "CPR12B",
    "CPR12C",
    "CPR21A",
    "CPR21B",
    "CPR21C",
    "CPR22A",
    "CPR22B",
    "CPR22C",
    "CCP11A",
    "CCP11B",
    "CCP12A",
    "CCP12B",
    "CCP21A",
    "CCP21B",
    "CCP22A",
    "CCP22B",
    "PCP1A",
    "PCP1B",
    "PCP2A",
    "PCP2B"
]


直流场电压模拟量_PPR = [
    "UDL_IN",
    "UDM_IN",
    "UDN_IN",
]

直流场电压模拟量_PPR_字段名 = [
    "PPR1A",
    "PPR1B",
    "PPR1C",
    "PPR2A",
    "PPR2B",
    "PPR2C"
]

换流变模拟量 = [
    "YY换流变中性点电流",
    "YD换流变中性点电流"
]

换流变模拟量_字段名 = [
    "CPR11A",
    "CPR11B",
    "CPR11C",
    "CPR12A",
    "CPR12B",
    "CPR12C",
    "CPR21A",
    "CPR21B",
    "CPR21C",
    "CPR22A",
    "CPR22B",
    "CPR22C"
]
log_list = []

def get_filename_keyword(name: str):
    if len(name) == 5:
        return "P{}{}{}1".format(name[3], name[:3], name[4])
    if len(name) == 6:
        return "P{}{}{}{}".format(name[3], name[:3], name[5], name[4])
    return name


def get_max(analog):
    if max(analog) > - min(analog):
        return max(analog)
    else:
        return min(analog)


def load_diagram(file_header: str):
    cfgFile = file_header + ".CFG"
    datFile = file_header + ".DAT"
    rec = Comtrade()
    rec.load(cfgFile, datFile)
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


def filter_files(directory, keywords):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_name = os.path.basename(filename)  # 获取文件名部分
            if all(keyword in file_name for keyword in keywords):
                files.append(os.path.abspath(os.path.join(root, filename)))
    return files

def get_analog_from_file(filepath):
    def _get_analog_from_file(字段, 量):
        data_list = []
        for i in 字段:
            files = filter_files(filepath, [get_filename_keyword(i), "Child0"])
            if len(files) <= 0:
                log_list.append("cannot find {}".format(i))
                continue
            path_without_extension, extension = os.path.splitext(files[0])
            rec = load_diagram(path_without_extension)
            data_list.append({
                "name": i,
                "data": get_analog(rec, 量)
            })
        return data_list

    return _get_analog_from_file

def find_diagram(filepath: str):
    log_list.clear()
    # 直流场电流模拟量
    func_get_analog_from_file = get_analog_from_file(filepath)
    直流场电流 = func_get_analog_from_file(直流场电流模拟量_字段名, 直流场电流模拟量)
    直流场电压 = func_get_analog_from_file(直流场电压模拟量_字段名, 直流场电压模拟量)
    直流场电压_PPR = func_get_analog_from_file(直流场电压模拟量_PPR_字段名, 直流场电压模拟量_PPR)
    换流变 = func_get_analog_from_file(换流变模拟量_字段名, 换流变模拟量)

    pass


def write_to_csv(filename: str, output_analog):
    f = open(filename, 'w', encoding='UTF8', newline='')

    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    for row in use_analog_list:
        for per in output_analog:
            if per["name"] == row:
                writer.writerow([per["name"], per["value"]])

    f.close()
