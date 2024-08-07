import csv
import os
import chardet
import concurrent.futures

def parallel_process(_process_file, all_files, progress_printer):
    result_data = []
    num_cpus = os.cpu_count()  # 获取 CPU 核心数
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_cpus) as executor:
        futures = {executor.submit(_process_file, file): file for file in all_files}
        for future in concurrent.futures.as_completed(futures):
            file = futures[future]
            try:
                data = future.result()
            except Exception as exc:
                progress_printer(f"处理{file}时发生异常: {exc}")
            else:
                result_data.append(data)
                progress_printer("", float(len(result_data) / float(len(all_files))))
    return result_data


def get_filename_keyword_with_pole(name: str):
    if len(name) == 6:
        return "{}{}1".format(name[:5], name[5])
    if len(name) == 7:
        return "{}{}{}".format(name[:5], name[6], name[5])
    return name


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

# def transform(des_file, res_file):
#     '''
#     将文件编码从 GBK 转换成 utf8
#     :param des_file: 待转换的编码为 GBK 的源文件
#     :param res_file: 转换之后的 utf8 编码的文件
#     :return: 
#     '''
#     with open(des_file, 'rb') as f:
#         data = f.read()
#     res = chardet.detect(data)
#     if res['encoding'] == 'GB2312':
#         res['encoding'] = 'GBK'
#     with open(res_file, 'w', encoding='utf-8') as file:
#         line = str(data, encoding=res['encoding'])
#         file.write(line)
    # print(line)

def transform(des_file, res_file):
    '''
    将文件编码从 GBK 转换成 utf8，并去掉每一行后面的空行
    :param des_file: 待转换的编码为 GBK 的源文件
    :param res_file: 转换之后的 utf8 编码的文件
    :return: 
    '''
    with open(des_file, 'rb') as f:
        data = f.read()
    res = chardet.detect(data)
    if res['encoding'] == 'GB2312':
        res['encoding'] = 'GBK'
    with open(res_file, 'wb') as file:
        lines = str(data, encoding=res['encoding']).splitlines()
        for line in lines:
            line = line.rstrip('\r\n')  # 去掉每一行后面的换行符和回车符
            file.write((line + '\n').encode('utf-8'))

def filter_files(directory, keywords) -> list[str]:
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_name = os.path.basename(filename)  # 获取文件名部分
            if all(keyword in file_name for keyword in keywords):
                files.append(os.path.abspath(os.path.join(root, filename)))
    return files


def convert_data_to_csv_style(dataname, data, transpose=True):
    all_names = set()
    for item in data:
        for sub_item in item['data']:
            all_names.add(sub_item['name'])

    rows = []
    for item in data:
        row = {'name': item['name']}
        for sub_item in item['data']:
            # 将 x 轴和 y 轴的数据交换
            row[sub_item['name']] = sub_item['value']
        # 没有的数据填空，不能没有key
        for name_key in all_names:
            if row.get(name_key) is None:
                row[name_key] = ""
        rows.append(row)

    if transpose:
        # 转置数据，交换 x 轴和 y 轴
        transposed_rows = []
        for name in all_names:
            transposed_row = {'name': name}
            for row in rows:
                transposed_row[row['name']] = row.get(name, '')
            transposed_rows.append(transposed_row)
        return {
            "dataname": dataname,
            "rows": rows,
            "data": transposed_rows,
            "lines": data[0]["row"]
        }
    else:
        return {
            "dataname": dataname,
            "rows": [{"name": name } for name in all_names],
            "data": rows,
            "lines": [i["name"] for i in data]
        }


def save_to_csv(data, csv_file_path):
    with open(csv_file_path, mode='w', encoding='gbk', newline='') as file:
        for i in data:
            writer = csv.DictWriter(file, fieldnames=['name'] + [row['name'] for row in i["rows"]])
            writer.writerow({"name": i["dataname"]})
            writer.writeheader()
            for line in i["lines"]:
                for j in i["data"]:
                    if j["name"] == line:
                        writer.writerow(j)
            # for row in i["data"]:
            #     writer.writerow(row)
            writer.writerow({"name": ""})

    print(f"CSV 文件已保存至 {csv_file_path}")

def convert_data_to_csv_2(data, csv_file_path):
    with open(csv_file_path, mode='w', encoding='gbk', newline='') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow([item['name']])
            all_names = set()
            for sub_item in item['data']:
                all_names.add(sub_item['name'])
            fieldnames = ['name'] + list(all_names)
            writer.writerow(fieldnames)
            for sub_item in item['data']:
                row = [sub_item['name']] + [sub_item['value'] for _ in range(len(all_names))]
                writer.writerow(row)
            writer.writerow([])  # 空行分隔不同数据

    print(f"CSV 文件已保存至 {csv_file_path}")



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

def remove_all_extensions(file_path):
    file_name, file_extension = os.path.splitext(file_path)
    while '.' in file_name:
        file_name, _ = os.path.splitext(file_name)
    return file_name