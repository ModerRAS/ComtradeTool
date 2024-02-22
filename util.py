import csv
import os
import chardet


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

def filter_files(directory, keywords):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_name = os.path.basename(filename)  # 获取文件名部分
            if all(keyword in file_name for keyword in keywords):
                files.append(os.path.abspath(os.path.join(root, filename)))
    return files


def convert_data_to_csv_style(dataname, data):
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
        rows.append(row)
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
