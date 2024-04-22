import json
import os
import zerorpc

zerorpc_server = "tcp://{}:4242".format(os.getenv('RPC_SERVER', "127.0.0.1"))
def get_analog_path_without_extension(name, path_without_extension: str, use_analog_list: list[str]):
    c = zerorpc.Client()
    c.connect(zerorpc_server)
    tmp = c.get_analog_path_without_extension(name, path_without_extension, list(use_analog_list))
    print(tmp)
    return tmp

def get_analog_raw(filepath: str, use_analog_list: list[str]):
    c = zerorpc.Client()
    c.connect(zerorpc_server)
    return c.get_analog_path_without_extension(filepath, list(use_analog_list))

