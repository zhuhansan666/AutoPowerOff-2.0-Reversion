from time import time

from logging import getLogger, basicConfig

from src.Tools import merge_dict
from src.debug import Debug

logger = getLogger("load")


class Load:
    def __init__(self, information_obj, app_config_obj, config_obj):
        self.__config = config_obj
        self.__debug = Debug(app_config_obj, config_obj)
        self.__information = information_obj

        self.__latest_wrote_time = time()

        self.default_config = app_config_obj.default_config

    def reload(self, rewrite_interval: int | float = 0):
        run_type = self.__config.load()
        if run_type[0] != 0:
            i = 1
            for error in run_type[1]:
                logger.error("读取配置文件发生错误(第{}个错误): errcode: {}, errinfo: {}".format(i, *error))
                i += 1
            del i

        # 便于人观看的配置
        result = merge_dict(self.__config.result, self.default_config)
        debug_result = self.__debug.reload()
        result["debug"] = debug_result

        self.__config.result = result.copy()  # 设置__config.result 以便__debug读取

        if abs(time() - self.__latest_wrote_time) > rewrite_interval:
            run_type = self.__config.write()
            if run_type[0] != 0:
                i = 1
                for error in run_type[1]:
                    logger.error("写入配置文件发生错误(第{}个错误): errcode: {}, errinfo: {}".format(i, *error))
                    i += 1
                del i
            self.__latest_wrote_time = time()

        # 程序可读取的配置
        result = result.copy()
        debug_result = self.__debug.reload(True)
        result["debug"] = debug_result
        self.__information.config = result.copy()

