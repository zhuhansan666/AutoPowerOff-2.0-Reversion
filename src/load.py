from src.Tools import merge_dict
from src.debug import Debug


class Load:
    def __init__(self, information_obj, app_config_obj, config_obj):
        self.__config = config_obj
        self.__debug = Debug(app_config_obj, config_obj)
        self.__information = information_obj

        self.default_config = app_config_obj.default_config

    def reload(self):
        self.__config.load()
        print(self.__config.result)

        # 便于人观看的配置
        result = merge_dict(self.__config.result, self.default_config)
        self.__config.result = result
        debug_result = self.__debug.reload()
        print(f"{debug_result =}")
        result["debug"] = debug_result
        # result["debug"] = self.__debug.default_debug
        print(1, result)
        self.__config.result = result.copy()
        # print(2, self.__config.result)
        self.__config.write()

        # # 程序可读取的配置
        # result = result.copy()
        # # debug_result = self.__debug.reload(True)
        # # result["debug"] = debug_result
        # self.__information.config = result
        #
        # # print(f"2 {self.__config.result = }")
