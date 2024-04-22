from pywebio.output import *

import sys

def print_log(log_str: str, progress=-1):
    if 'unittest' in sys.modules.keys():
        print(log_str)
    elif progress!=-1:
        set_progressbar("Progress", progress)
    else:
        put_markdown(log_str)