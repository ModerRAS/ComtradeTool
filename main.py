import datetime
import os
import random
import shutil
import string
import time
import zipfile
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import info as session_info
from pywebio.session import go_app

from diagram import find_diagram, find_diagram_hlb2, generate_all_harmonic_list_csv, get_DC_field_analog_quantity, get_hlb1_analog_quantity
from build_time import *
from log import print_log

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created.")
    else:
        print(f"Directory '{directory}' already exists.")


def unzip_file(zip_file_path, extract_to_folder):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_folder)

def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def t(eng, chinese):
    """return English or Chinese text according to the user's browser language"""
    return chinese if 'zh' in session_info.user_language else eng

def delete_file_or_folder(path):
    """删除文件或文件夹"""
    if os.path.isfile(path):
        os.remove(path)
        print(f'文件 {path} 已删除。')
    elif os.path.isdir(path):
        shutil.rmtree(path)
        print(f'文件夹 {path} 及其内容已删除。')
    else:
        print(f'路径 {path} 不是有效的文件或文件夹路径。')


def list_files_in_folder(folder_path):
    """
    列出文件夹中的所有文件。

    参数：
    folder_path (str): 要列出文件的文件夹路径。

    返回：
    list: 包含文件名的列表。
    """
    files_and_folders = os.listdir(folder_path)
    files = [f for f in files_and_folders if os.path.isfile(os.path.join(folder_path, f))]
    return files

def manual_upload_process(process_func=find_diagram):
    file_list = list_files_in_folder("/tmp/upload")
    file_selected = select("选择文件", file_list)
    start_time = time.time()
    put_progressbar("Progress", 0, "进度")
    print_log("开始", 0.01)
    random_name = generate_random_string(10)
    unzip_file('/tmp/upload/'+ file_selected, '/tmp/'+ random_name)
    process_func('/tmp/'+ random_name, csv_path='/tmp/'+ random_name + ".csv")
    content = open('/tmp/'+ random_name + ".csv", 'rb').read()
    put_markdown("清理临时文件")
    delete_file_or_folder('/tmp/'+ random_name)
    delete_file_or_folder('/tmp/'+ random_name + ".csv")
    end_time = time.time()
    # 计算时间差
    elapsed_time = end_time - start_time
    put_markdown(f"程序运行时间为：{elapsed_time} 秒")
    return content
def process_content(process_func=find_diagram):
    f = file_upload("上传波形文件压缩包", accept="application/zip")
    start_time = time.time()
    put_progressbar("Progress", 0, "进度")
    random_name = generate_random_string(10)
    open('/tmp/'+ random_name + ".zip", 'wb').write(f['content'])
    unzip_file('/tmp/'+ random_name + ".zip", '/tmp/'+ random_name)
    process_func('/tmp/'+ random_name, csv_path='/tmp/'+ random_name + ".csv")
    content = open('/tmp/'+ random_name + ".csv", 'rb').read()
    put_markdown("清理临时文件")
    delete_file_or_folder('/tmp/'+ random_name + ".zip")
    delete_file_or_folder('/tmp/'+ random_name)
    delete_file_or_folder('/tmp/'+ random_name + ".csv")
    end_time = time.time()
    # 计算时间差
    elapsed_time = end_time - start_time
    put_markdown(f"程序运行时间为：{elapsed_time} 秒")
    return content

def 小定值零飘检查():
    """分析波形的简单应用
    """

    put_markdown(t("""
    """, """
# 模拟量检查工具
用于自动生成小定值零飘检查需要的表格文件
将下载的内置录波谱图文件夹打包成zip文件，然后上传，请勿更改谱图文件名
文件夹层级任意
    """))

    content = process_content(find_diagram)
    put_file("小定值保护模拟量零漂检查{}.csv".format(time.strftime("%Y-%m")), content, '点击下载CSV文件')

def 模拟量检查():
    """分析波形的简单应用
    """

    put_markdown(t("""
    """, """
# 模拟量检查工具
用于自动生成直流场模拟量检查需要的表格文件
将下载的内置录波谱图文件夹打包成zip文件，然后上传，请勿更改谱图文件名
文件夹层级任意
    """))

    content = process_content(get_DC_field_analog_quantity)
    put_file("直流场模拟量检查{}.csv".format(time.strftime("%Y-%m")), content, '点击下载CSV文件')

def 换流变1模拟量检查():
    """分析波形的简单应用
    """

    put_markdown(t("""
    """, """
# 模拟量检查工具
用于自动生成换流变1模拟量检查需要的表格文件
将下载的内置录波谱图文件夹打包成zip文件，然后上传，请勿更改谱图文件名
文件夹层级任意
    """))

    content = process_content(get_hlb1_analog_quantity)
    put_file("换流变1模拟量检查{}.csv".format(time.strftime("%Y-%m")), content, '点击下载CSV文件')


def 换流变2模拟量检查():
    """分析波形的简单应用
    """

    put_markdown(t("""
    """, """
# 模拟量检查工具
用于自动生成换流变2模拟量检查需要的表格文件
将下载的内置录波谱图文件夹打包成zip文件，然后上传，请勿更改谱图文件名
文件夹层级任意
    """))

    content = process_content(find_diagram_hlb2)
    put_file("换流变2模拟量检查{}.csv".format(time.strftime("%Y-%m")), content, '点击下载CSV文件')

def 换流变谐波分析():
    """分析波形的简单应用
    """

    put_markdown(t("""
    """, """
# 换流变谐波分析工具
用于自动生成换流变谐波分析所需要的表格文件
将下载的外置录波谱图文件夹打包成zip文件，然后上传，请勿更改谱图文件名
文件夹层级任意
    """))

    content = manual_upload_process(generate_all_harmonic_list_csv(False))
    put_file("换流变谐波分析{}.csv".format(time.strftime("%Y-%m")), content, '点击下载CSV文件')


def 换流变谐波分析_fft():
    """分析波形的简单应用
    """

    put_markdown(t("""
    """, """
# 换流变谐波分析工具傅立叶变换版
用于自动生成换流变谐波分析所需要的表格文件
将下载的外置录波谱图文件夹打包成zip文件，然后上传，请勿更改谱图文件名
文件夹层级任意
    """))

    content = manual_upload_process(generate_all_harmonic_list_csv(True))
    put_file("换流变谐波分析{}.csv".format(time.strftime("%Y-%m")), content, '点击下载CSV文件')




def index():
    put_markdown("# 模拟量检查工具")
    put_buttons(['点击进入小定值零飘检查（月度）'], [lambda: go_app('小定值零飘检查', new_window=False)])
    put_buttons(['点击进入模拟量检查（季度）'], [lambda: go_app('模拟量检查', new_window=False)])
    put_buttons(['点击进入换流变1模拟量检查（季度）'], [lambda: go_app('换流变1模拟量检查', new_window=False)])
    put_buttons(['点击进入换流变谐波分析'], [lambda: go_app('换流变谐波分析', new_window=False)])
    put_buttons(['点击进入换流变谐波分析傅立叶变换版'], [lambda: go_app('换流变谐波分析_fft', new_window=False)])
    put_markdown("构建于{}".format(formatted_time))

if __name__ == '__main__':
    create_directory_if_not_exists("/tmp/upload")
    start_server([index,小定值零飘检查, 模拟量检查, 换流变1模拟量检查, 换流变2模拟量检查, 换流变谐波分析, 换流变谐波分析_fft], debug=True, port=23080, cdn=False, max_payload_size='500M')
