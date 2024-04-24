from pywebio.output import *

import sys

def print_log(log_str: str, progress=-1.0):
    if 'unittest' in sys.modules.keys():
        print(log_str)
    elif progress>=0:
        set_progressbar("Progress", progress)
        print(log_str)
    else:
        put_markdown(log_str)