import json
import os
import xmlrpc.client

rpc_server = "http://{}:4242".format(os.getenv('RPC_SERVER', "127.0.0.1"))
def get_analog_path_without_extension(name, path_without_extension: str, use_analog_list: list[str]):
    proxy = xmlrpc.client.ServerProxy(rpc_server)
    tmp = proxy.get_analog_path_without_extension(name, path_without_extension, list(use_analog_list))
    print(tmp)
    return tmp

def get_analog_raw(filepath: str, use_analog_list: list[str]):
    proxy = xmlrpc.client.ServerProxy(rpc_server)
    return proxy.get_analog_path_without_extension(filepath, list(use_analog_list))

