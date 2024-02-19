# import matplotlib.pyplot as plt
import time
import chardet
from comtrade import Comtrade
import csv
import os
import codecs

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
    "PPR1A",
    "PPR1B",
    "PPR1C",
    "PPR2A",
    "PPR2B",
    "PPR2C"
]


直流场电压模拟量_PCP_CCP = [
    "UDL_IN",
    "UDM_IN",
    "UDN_IN",
]

直流场电压模拟量_PCP_CCP_字段名 = [
    "PCP1A",
    "PCP1B",
    "PCP2A",
    "PCP2B",
    "CCP11A",
    "CCP11B",
    "CCP12A",
    "CCP12B",
    "CCP21A",
    "CCP21B",
    "CCP22A",
    "CCP22B",
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

def transform(des_file, res_file):
    '''
    将文件编码从 GBK 转换成 utf8
    :param des_file: 待转换的编码为 GBK 的源文件
    :param res_file: 转换之后的 utf8 编码的文件
    :return: 
    '''
    with open(des_file, 'rb') as f:
        data = f.read()
    res = chardet.detect(data)
    if res['encoding'] == 'GB2312':
        res['encoding'] = 'GBK'
    with open(res_file, 'w', encoding='utf-8') as file:
        line = str(data, encoding=res['encoding'])
        file.write(line)
    # print(line)

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


def filter_files(directory, keywords):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_name = os.path.basename(filename)  # 获取文件名部分
            if all(keyword in file_name for keyword in keywords):
                files.append(os.path.abspath(os.path.join(root, filename)))
    return files

def get_analog_from_file(filepath):
    def _get_analog_from_file(字段, 量, Child="Child0"):
        data_list = []
        for i in 字段:
            files = filter_files(filepath, [get_filename_keyword(i), Child])
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

def convert_data_to_csv(data, csv_file_path):
    all_names = set()
    for item in data:
        for sub_item in item['data']:
            all_names.add(sub_item['name'])

    rows = []
    for item in data:
        row = {'name': item['name']}
        for sub_item in item['data']:
            row[sub_item['name']] = sub_item['value']
        rows.append(row)

    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['name'] + list(all_names))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"CSV 文件已保存至 {csv_file_path}")

def find_diagram(filepath: str):
    start_time = time.time()
    log_list.clear()
    # 直流场电流模拟量
    func_get_analog_from_file = get_analog_from_file(filepath)
    直流场电流 = func_get_analog_from_file(直流场电流模拟量_字段名, 直流场电流模拟量)
    直流场电压 = func_get_analog_from_file(直流场电压模拟量_字段名, 直流场电压模拟量)
    直流场电压_PCP_CCP = func_get_analog_from_file(直流场电压模拟量_PCP_CCP_字段名, 直流场电压模拟量_PCP_CCP)
    换流变 = func_get_analog_from_file(换流变模拟量_字段名, 换流变模拟量, Child="Child2")

    print(直流场电压)
    convert_data_to_csv(直流场电压, '直流场电压.csv')

    end_time = time.time()
    # 计算时间差
    elapsed_time = end_time - start_time
    print(f"程序运行时间为：{elapsed_time} 秒")
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

if __name__ == '__main__':
    find_diagram(r"C:\WorkSpace\Recoder\20231006test")