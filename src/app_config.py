from os import getenv, path

from logging import DEBUG, INFO, WARNING, ERROR
from time import time, strftime, localtime


class AppConfig:
    def __init__(self):
        self.VERSION = (1, 0, 0, 20221030_110000)
        self.github_url = "https://github.com/zhuhansan666/AutoPowerOff-2.0-Reversion"

        appdata = getenv("appdata", None)
        if appdata is None:
            appdata = "./"
        else:
            appdata = path.join(appdata, "./AutoPowerOff-2")
        self.config_file = path.abspath(path.normpath(path.join(appdata, "./Config/Config.json")))

        self.log_file = None

        tmp = getenv("tmp", None)
        if tmp is None:
            tmp = "./"

        self.cmd_temppath = path.abspath(path.normpath(tmp))

        self.ua = {}
        self.get_time_url = ["https://www.tsa.cn/api/time/getCurrentTime", "ms"]

        self.default_config = {
            "apo-time": "17:00:00",
            "apo-must-time": "17:20:00",
            "timeout": 60,
            "after-fullscreen-timeout": 10,
            "ui-timeout": 30,
            "ui-after-fullscreen-timeout": 10
        }
        self.default_debug = {
            "out-log": True,
            "log-level": INFO,
        }

        self.log_filename = '{}'.format(strftime("./log/%Y-%m-%d.log", localtime()))

        self.reload_file_interval: float | int = 0.5
        self.rewrite_file_interval: float | int = 1


if __name__ == '__main__':
    test = AppConfig()
    print(test.__dict__)
