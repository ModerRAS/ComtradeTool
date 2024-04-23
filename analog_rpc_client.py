import base64
import pickle
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
    return pickle.loads(base64.b64decode(proxy.get_analog_raw(filepath, use_analog_list)))

def calculate_harmonic(voltage, harmonic_order, xx = 0, cyc_sample=100):
    proxy = xmlrpc.client.ServerProxy(rpc_server)
    return proxy.calculate_harmonic(base64.b64encode(pickle.dumps(voltage)).decode("utf-8"), harmonic_order, xx, cyc_sample)
