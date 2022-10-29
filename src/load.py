from src.init import config
from src.g import information

from src.Tools import merge_dict
from src.debug import Debug


class Load:
    def __init__(self):
        self.__config = config
        self.__debug = Debug()
        self.__information = information

        self.default_config = {
            "apo-time": "17:00:00",
            "apo-must-time": "17:20:00",
            "timeout": 60,
            "after-fullscreen-timeout": 10,
        }

    def reload(self):
        self.__config.load()

        # 程序可读取的配置
        result = merge_dict(self.__config.result, self.default_config)
        debug_result = self.__debug.reload()
        result["debug"] = debug_result
        self.__information.config = result.copy()

        # 便于人观看的配置
        debug_result = self.__debug.reload(True)
        result["debug"] = debug_result
        self.__config.result = result.copy()
        self.__config.write()

if __name__ == '__main__':
    test = Load()
    test.reload()
