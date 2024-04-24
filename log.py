import os
from pywebio.output import *

def print_log(log_str: str, progress=-1.0):
    
    if int(os.getenv('unittest', 0)) != 0:
        print(log_str)
        return
    if progress>=0:
        set_progressbar("Progress", progress)
        print("{}, {}".format(log_str, progress))
    else:
        put_markdown(log_str)