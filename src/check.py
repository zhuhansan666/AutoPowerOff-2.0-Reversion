import time
from typing import Iterable

from src.get_time import get_time
from src.uis.gtools import *

from logging import getLogger

from win32gui import GetActiveWindow, GetForegroundWindow, GetWindowRect
import keyboard
# from pynput import mouse

logger = getLogger("check")


class Check:
    """
        检测是否处于合法关机时间内
    """

    def __init__(self, information_obj, events_information_obj):
        self.mouse_check_thread = None
        self.keyboard_check_thread = None

        self.__information = information_obj
        self.__events_information = events_information_obj

        self.shutdown_code = 0

        self.timeout = 0

        self.arrived_shutdown_time = 0

        self.fullscreen_app = [False, 0, 0]  # 是否开启, 开启的时间, 关闭的时间

        self.latest_keyboard_mouse_event_time = self.get_time(False)  # 上一次按键操作时间

        self.check_keyboard_events_thread()

        self.ui_obj = None

    @staticmethod
    def get_time(_format: bool = True) -> str | int | float:
        result = get_time()
        if result[0] == 0:  # 请求失败则使用本地时间
            if _format:
                localtime = time.localtime(result[-1])
            else:
                return result[-1]
        else:
            if _format:
                localtime = time.localtime()
            else:
                return time.time()
        time_string = time.strftime("%H:%M:%S", localtime)
        return time_string

    @staticmethod
    def __check_time_size(now: Iterable, target: Iterable):
        """
            比较时间, 若到达或超过target则return True, now, target均为[%H, %M, %S]
        """
        for n, t in zip(now, target):
            if n < t:
                return False
        return True

    def __check_fullscreen_app(self):
        scr_size = get_screen_size()  # 获取缩放后的大小
        active_win = foreground_win = 0
        active_winsize = foreground_winsize = None
        error = RuntimeError("未获取到ERROR")
        for _ in range(3):
            try:
                active_win = GetActiveWindow()
                logger.debug(f"获取 ActiveWindow (在第 {_ + 1} 次) 成功")
                break
            except Exception as e:
                error = e
        else:
            logger.error("获取 ActiveWindow 错误", exc_info=error)
        for _ in range(3):
            try:
                foreground_win = GetForegroundWindow()
                logger.debug(f"获取 ForegroundWindow (在第 {_ + 1} 次) 成功")
                break
            except Exception as e:
                error = e
        else:
            logger.error("获取 ForegroundWindow 错误", exc_info=error)

        if active_win != 0:
            for _ in range(3):
                try:
                    active_winsize = GetWindowRect(active_win)[2:]
                    logger.debug("获取 GetWindowRect (active_win: {}) (在第 {} 次) 成功".format(active_win, _ + 1))
                    break
                except Exception as e:
                    error = e
            else:
                logger.debug("获取 GetWindowRect (active_win: {}) 错误".format(active_win), exc_info=error)

        if foreground_win != 0:
            for _ in range(3):
                try:
                    foreground_winsize = GetWindowRect(foreground_win)[2:]
                    logger.debug("获取 GetWindowRect (foreground: {}) (在第 {} 次) 成功".format(foreground_win, _ + 1))
                    break
                except Exception as e:
                    error = e
            else:
                logger.error("获取 GetWindowRect (foreground: {}) 错误".format(foreground_win), exc_info=error)

        bool_lst = []
        if active_winsize is not None:
            bool_lst.append(check_winsize(active_winsize, scr_size))
        if foreground_winsize is not None:
            bool_lst.append(check_winsize(foreground_winsize, scr_size))

        fullscreen = any(bool_lst)
        if fullscreen is True:
            self.fullscreen_app[0], self.fullscreen_app[1] = fullscreen, self.get_time(False)
            logger.debug("全屏应用程序开启")
        else:
            if self.fullscreen_app[0]:
                self.fullscreen_app[0], self.fullscreen_app[2] = False, self.get_time(False)
                logger.debug("全屏应用程序关闭")

    def __call_ui(self, timeout: int | float):
        # print("CallUi", timeout)
        if self.ui_obj is not None:
            return self.ui_obj.mainloop(timeout)
        return 0

    def __timecheck(self):
        times = self.get_time().split(":")
        times = [int(t) for t in times]
        target_times = self.__information.config["apo-time"].split(":")  # 关机时间
        target_times = [int(_t) for _t in target_times]
        target_times2 = self.__information.config["apo-must-time"].split(":")
        target_times2 = [int(_t) for _t in target_times2]  # 强制关机时间
        apo_1 = self.__check_time_size(times, target_times)
        apo_2 = self.__check_time_size(times, target_times2)

        if apo_1 is True and apo_2 is not True:  # 关机~强制关机之间
            if self.arrived_shutdown_time == 0:
                logger.info("到达关机时间 ({})".format(self.__information.config["apo-time"]))
                self.arrived_shutdown_time = 1

            if not self.fullscreen_app[0] and self.get_time(False) - self.fullscreen_app[2] <= \
                    self.__information.config["after-fullscreen-timeout"] + 3:  # 如果刚刚关闭了全屏应用
                if self.latest_keyboard_mouse_event_time != 0 and \
                        self.get_time(False) - self.latest_keyboard_mouse_event_time >= \
                        self.__information.config["after-fullscreen-timeout"]:
                    ui_timeout = self.__information.config["ui-after-fullscreen-timeout"]
                    self.shutdown_code = 2
                    result = self.__call_ui(ui_timeout)
                    if result == 1:
                        logger.debug("(刚刚关闭了全屏应用) 选定关机或超时")
                        self.__events_information.shutdown = True
                    elif result == 2:
                        logger.debug("(刚刚关闭了全屏应用) 取消关机")
                        self.__information.exit = True
                    else:
                        logger.debug("(刚刚关闭了全屏应用) 后台运行")
                        self.latest_keyboard_mouse_event_time = self.get_time(False)
                        self.fullscreen_app = [False, 0, 0]
            elif not self.fullscreen_app[0]:  # 全屏应用未打开
                if self.latest_keyboard_mouse_event_time != 0 and \
                        self.get_time(False) - self.latest_keyboard_mouse_event_time >= self.__information.config["timeout"]:
                    ui_timeout = self.__information.config["ui-timeout"]
                    self.shutdown_code = 1
                    result = self.__call_ui(ui_timeout)
                    if result == 1:
                        logger.debug("(正常模式) 选定关机或超时")
                        self.__events_information.shutdown = True
                    elif result == 2:
                        logger.debug("(正常模式) 取消关机")
                        self.__information.exit = True
                    else:
                        logger.debug("(正常模式) 后台运行")
                        self.latest_keyboard_mouse_event_time = self.get_time(False)
        elif apo_2 is True:  # 强制关机
            if self.arrived_shutdown_time != 2:
                self.arrived_shutdown_time = 2
                logger.info("到达强制关机时间 ({})".format(self.__information.config["apo-must-time"]))
            self.shutdown_code = 3

    def __keyboard_events(self, key):
        self.latest_keyboard_mouse_event_time = self.get_time(False)

    def __mouse_events(self, *event):
        print(event)
        self.latest_keyboard_mouse_event_time = self.get_time(False)

    def check_keyboard_events_thread(self):
        # self.keyboard_check_thread = keyboard.Listener(on_press=self.__keyboard_events,
        #                                                on_release=self.__keyboard_events, daemon=True, suppress=False)
        # self.keyboard_check_thread.start()
        keyboard.hook(self.__keyboard_events)

        # The event listener will be running in this block
        # with mouse.Events() as events:
        #     # Block at most one second
        #     event = events.get(1.0)
        #     if event is None:
        #         print('You did not interact with the mouse within one second')
        #     else:
        #         print('Received event {}'.format(event))

        # self.mouse_check_thread = mouse.Listener(on_move=self.__mouse_events, on_click=self.__mouse_events,
        #                                          on_scroll=self.__mouse_events, daemon=True, suppress=False)
        # mouse.hook(self.__mouse_events)

        # self.mouse_check_thread.start()

        # self.keyboard_check_thread.stop()
        # self.mouse_check_thread.stop()

    def exit(self):
        ...

    def check(self) -> int:
        """
            检测是否处于合法关机状态
            :return int, 0 -> 不在关机状态, 1~2 -> 在关机状态(1: 正常; 2: 在全屏应用后), 3 -> 到达强制关机状态
        """
        self.__check_fullscreen_app()
        self.__timecheck()
        return self.shutdown_code
