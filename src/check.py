import time
from typing import Iterable

from g import information


class Check:
    """
        检测是否处于合法关机时间内
    """

    def __init__(self):
        self.__config = information
        self.__config.config = {
            "apo-time": "15:18:00",
            "apo-must-time": "17:20:00",
            "timeout": 60,
            "after-fullscreen-timeout": 10,
            "debug": {
                "out-log": False,
                "log-level": "INFO"
            }
        }

        self.shutdown_code = 0

        self.timeout = 0

    @staticmethod
    def get_time() -> str:
        test = time.strftime("%H:%M:%S", time.localtime())
        return test

    @staticmethod
    def __check_time_size(now: Iterable, target: Iterable):
        """
            比较时间, 若到达或超过target则return True, now, target均为[%H, %M, %S]
        """
        for n, t in zip(now, target):
            if n < t:
                return False
        return True

    def __timecheck(self):
        times = self.get_time().split(":")
        times = [int(t) for t in times]
        target_times = self.__config.config["apo-time"].split(":")  # 关机时间
        target_times = [int(_t) for _t in target_times]
        target_times2 = self.__config.config["apo-must-time"].split(":")
        target_times2 = [int(_t) for _t in target_times]  # 强制关机时间
        apo_1 = self.__check_time_size(times, target_times)
        apo_2 = self.__check_time_size(times, target_times2)
        if apo_1 is True and apo_2 is not True:  # 关机-强制关机之间
            ...
        elif apo_2 is True:  # 强制关机
            self.shutdown_code = 2


    def check(self) -> int:
        """
            检测是否处于合法关机状态
            :return int, 0 -> 不在关机状态, 1 -> 在关机状态, 2 -> 到达强制关机状态
        """
        return self.shutdown_code


if __name__ == '__main__':
    test = Check()
    while True:
        test._Check__timecheck()
        time.sleep(1)
