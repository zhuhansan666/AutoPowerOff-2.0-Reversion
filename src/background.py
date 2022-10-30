from src.check import Check

from subprocess import run

from logging import getLogger
from time import time as get_time
from threading import Thread
from time import sleep

logger = getLogger("BackGround")

DEBUG = True
if DEBUG:
    print("In Debug Mode!")


class BackGround:
    def __init__(self, check_obj: Check, events_information_obj, load_obj, app_config_obj):
        self.__check = check_obj
        self.__events_information = events_information_obj
        self.__load = load_obj
        self.__app_config = app_config_obj

        self.running = True

        self.__reload_thread = Thread(target=lambda: self.__reload(app_config_obj.reload_file_interval), daemon=True)
        self.__reload_thread.start()

    def __reload(self, interval: int | float):
        while self.running:
            sleep(interval)
            self.__load.reload()

    def exit(self):
        self.running = False

    @staticmethod
    def __shutdown():
        run("shutdown /f /s /t 0")

    def mainloop(self):
        while self.running:
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
            sleep(0.5)
