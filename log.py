from pywebio.output import *

import sys

def print_log(log_str: str, progress=-1.0):
    # if 'unittest' in sys.modules.keys():
    #     print("单元测试:{}, {}".format(log_str, __name__))
    if progress>=0:
        set_progressbar("Progress", progress)
        print("{}, {}".format(log_str, progress))
    else:
        put_markdown(log_str)