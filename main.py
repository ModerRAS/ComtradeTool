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

from diagram import find_diagram

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

def main():
    """分析波形的简单应用
    """

    put_markdown(t("""
    """, """
# 模拟量检查工具
用于自动生成小定值零飘检查需要的表格文件
将下载的内置录波谱图文件夹打包成zip文件，然后上传，请勿更改导出文件名
文件夹层级任意
    """))

    f = file_upload("上传波形文件压缩包", accept="application/zip")
    start_time = time.time()
    put_markdown("处理中。。。。。。")
    random_name = generate_random_string(10)
    open('/tmp/'+ random_name + ".zip", 'wb').write(f['content'])
    unzip_file('/tmp/'+ random_name + ".zip", '/tmp/'+ random_name)
    find_diagram('/tmp/'+ random_name, csv_path='/tmp/'+ random_name + ".csv")
    content = open('/tmp/'+ random_name + ".csv", 'rb').read()
    put_markdown("清理临时文件")
    delete_file_or_folder('/tmp/'+ random_name + ".zip")
    delete_file_or_folder('/tmp/'+ random_name)
    delete_file_or_folder('/tmp/'+ random_name + ".csv")
    end_time = time.time()
    # 计算时间差
    elapsed_time = end_time - start_time
    put_markdown(f"程序运行时间为：{elapsed_time} 秒")
    put_file(random_name + ".csv", content, '点击下载CSV文件')


if __name__ == '__main__':
    start_server(main, debug=True, port=23080)