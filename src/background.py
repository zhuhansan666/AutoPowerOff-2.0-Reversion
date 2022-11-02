from src.check import Check

from subprocess import run

from logging import getLogger, getLevelName, basicConfig
from time import time as get_time
from os import path
from threading import Thread
from time import sleep

logger = getLogger("BackGround")

DEBUG = True if path.splitext(__file__)[-1] == ".py" else False
if DEBUG:
    print("In Debug Mode!")


class BackGround:
    def __init__(self, exit_func, check_obj: Check, events_information_obj, load_obj, app_config_obj, information_obj):
        self.__exit_func = exit_func

        self.__check = check_obj
        self.__information = information_obj
        self.__events_information = events_information_obj
        self.__load = load_obj
        self.__app_config = app_config_obj

        self.__log_configs = {
            "low-level": None
        }

        self.running = True

        self.__reload_thread = Thread(name="reload", target=lambda: self.__reload(app_config_obj.reload_file_interval,
                                                                                  app_config_obj.rewrite_file_interval),
                                      daemon=True)
        self.__reload_thread.start()

    def __reload(self, interval: int | float, rewrote_interval: int | float):
        while self.running:
            sleep(interval)
            self.__load.reload(rewrote_interval)

    def exit(self):
        self.running = False

    @staticmethod
    def __shutdown():
        run("shutdown /f /s /t 0")

    def __set_loglevel(self):
        log_level = self.__information.config["debug"]["log-level"]
        print(log_level)
        if log_level != self.__log_configs.get("low-level", None) or self.__log_configs.get("low-level", None) is None:
            self.__log_configs["low-level"] = log_level
            basicConfig(level=log_level)

    def mainloop(self):
        while self.running:
            if self.__events_information.exit:
                try:
                    self.__exit_func()
                except Exception as e:
                    logger.error("运行退出程序发生错误: ", exc_info=e)

            try:
                self.__set_loglevel()
            except Exception as e:
                logger.error("后台线程mainloop 重设置日志级别发生错误:", exc_info=e)

            try:
                self.__events_information.shutdown_type = self.__check.check()
                if self.__events_information.shutdown_type != 0:
                    if self.__events_information.shutdown_type == 1:
                        self.__events_information.shutdown_info = "检测到您长时间无操作, 是否关机?"
                    elif self.__events_information.shutdown_type == 2:
                        self.__events_information.shutdown_info = "您刚刚关闭了全屏应用, 是否关机?"
                    elif self.__events_information.shutdown_type == 3:
                        self.__events_information.shutdown_info = "正在强制关机中~ 请稍后..."
                else:
                    self.__events_information.shutdown_info = ""
                if self.__events_information.shutdown is True:
                    logger.info("关机...")
                    self.exit()
                    if not DEBUG:
                        self.__shutdown()
                    else:
                        print("DEBUG: Shutdown (Will not true shutdown)...")
                    self.__events_information.exit = True
            except Exception as e:
                logger.error(msg="后台线程mainloop发生错误: ", exc_info=e)
            sleep(0.5)
