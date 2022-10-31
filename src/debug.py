from logging import DEBUG, INFO, WARNING, ERROR

from src.Tools import merge_dict


class Debug:
    def __init__(self, app_config_obj, config_obj):
        self.__config = config_obj

        self.default_debug = app_config_obj.default_debug

        self.log_levels = {
            "DEBUG": DEBUG,
            "INFO": INFO,
            "WARNING": WARNING,
            "ERROR": ERROR,
        }
        self.log_level_string = False

    def __decode_log_level(self, dic: dict):
        """
            处理log-level, 将其从str转int, 未知则使用默认
        """
        dic = dic.copy()  # 防止直接操作

        log_level = dic.get("log-level", None)
        default: int = self.default_debug.get("log-level")  # 默认log-level
        if log_level is None:  # 为空则使用默认
            log_level: None
            dic["log-level"] = default
        elif type(log_level) == str:  # 为字符串就行转移
            log_level: str
            for k, v in self.log_levels.items():
                if log_level.upper().replace(" ", "") == k:  # 在字符串中使用对应级别
                    dic["log-level"] = v
                    break
            else:  # 不在字符串中使用默认
                dic["log-level"] = default
            self.log_level_string = True
        elif type(log_level) == int:
            if log_level not in self.log_levels.values():  # 不在指定的级别中使用默认
                dic["log-level"] = default
        else:  # 什么都不是使用默认
            dic["log-level"] = default

        return dic

    # def __encode_log_level(self, dic: dict):
    #     """
    #         处理log-level, 将其从int转str, 未知则使用默认
    #     """
    #     dic = dic.copy()  # 防止直接操作
    #     if self.log_level_string:
    #         log_level = dic.get("log-level", None)
    #         default: int = self.default_debug.get("log-level")  # 默认log-level
    #         default: list = [k for k, v in self.log_levels.items() if v == default]
    #         if len(default) > 0:
    #             default = default[0]
    #             default: str
    #         else:
    #             default: int
    #
    #         for k, v in self.log_levels.items():
    #             if log_level == v:  # 在字符串中使用对应级别
    #                 dic["log-level"] = k
    #                 break
    #         else:  # 不在字符串中使用默认
    #             dic["log-level"] = default
    #
    #     return dic

    def reload(self, decode: bool = False):
        print(f"debug -> {self.__config.result}")
        result = merge_dict(self.__config.result.get("debug", {}), self.default_debug)
        if decode:
            result = self.__decode_log_level(result)
        self.__config.result["debug"] = result

        return result
