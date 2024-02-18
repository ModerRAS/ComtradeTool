from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import info as session_info



def t(eng, chinese):
    """return English or Chinese text according to the user's browser language"""
    return chinese if 'zh' in session_info.user_language else eng


def main():
    """分析波形的简单应用
    """

    put_markdown(t("""
    """, """
# 模拟量检查工具
用于自动生成小定值零飘检查需要的表格文件
    """))

    info = input_group(t('', '波形路径：'), [
        input(t("Your Comtrade file folder", "请输入从后台导出的波形路径"), name="filepath"),
    ])


if __name__ == '__main__':
    start_server(main, debug=True, port=23080)