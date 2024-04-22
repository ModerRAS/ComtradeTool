import zerorpc
from comtrade import Comtrade

from util import get_max, transform


class AnalogRpcServer(object):
    def load_diagram(self, file_header: str):
        cfgFile = file_header + ".CFG"
        datFile = file_header + ".DAT"
        rec = Comtrade()
        try:
            rec.load(cfgFile, datFile)
        except UnicodeDecodeError as e:
            ocfgfile = cfgFile + "cfg"
            transform(cfgFile,ocfgfile)
    
            rec.load(ocfgfile, datFile)
        return rec
    
    
    def get_analog(self, rec: Comtrade, use_analog_list: list[str]):
        analog_list = []
        # 模拟通道的数量
        analog_count = rec.analog_count
        # 循环获取模拟通道的名称
        for i in range(analog_count):
            chan = rec.analog_channel_ids[i]
            if chan in use_analog_list:
                analog_list.append({
                    "name": chan,
                    "id": i
                })
        output_analog = []
        # 循环输出81个模拟量通道的采集数据
        for use_analog in analog_list:
            max_value = get_max(rec.analog[use_analog["id"]])
            output_analog.append({
                "name": use_analog["name"],
                "value": max_value
            })
            # print(max([abs(), abs(min(analog))]))
        return output_analog
    def get_analog_path_without_extension(self, name, path_without_extension: str, use_analog_list: list[str]):
        rec = self.load_diagram(path_without_extension)
        return {
                "name": name,
                "data": self.get_analog(rec, use_analog_list),
                "row": use_analog_list
            }
    
    def get_analog_raw(self, filepath: str, use_analog_list: list[str]):
        rec = self.load_diagram(filepath)
        analog_list = []
        # 模拟通道的数量
        analog_count = rec.analog_count
        # 循环获取模拟通道的名称
        for i in range(analog_count):
            chan = rec.analog_channel_ids[i]
            if chan in use_analog_list:
                analog_list.append({
                    "name": chan,
                    "id": i
                })
        output_analog = []
        # 循环输出81个模拟量通道的采集数据
        for use_analog in analog_list:
            output_analog.append({
                "name": use_analog["name"],
                "value": rec.analog[use_analog["id"]]
            })
            # print(max([abs(), abs(min(analog))]))
        return output_analog



if __name__ == '__main__':
    # 创建 ZeroRPC 服务器并运行
    server = zerorpc.Server(AnalogRpcServer())
    server.bind("tcp://0.0.0.0:4242")
    server.run()