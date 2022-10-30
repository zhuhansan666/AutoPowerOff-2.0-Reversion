import win32api
import win32con
import win32gui

from logging import getLogger
from time import sleep

logger = getLogger("get_shutdown")


class ShutdownEvent:
    def __init__(self, callback=None):
        self.running = True
        self.callback = callback

        h_inst = win32api.GetModuleHandle(None)
        wndclass = win32gui.WNDCLASS()
        wndclass.hInstance = h_inst
        wndclass.lpszClassName = "GetShutdownEvent"
        messageMap = {
            win32con.WM_QUERYENDSESSION: self.shutdown_event,
            win32con.WM_ENDSESSION: self.shutdown_event,
        }

        wndclass.lpfnWndProc = messageMap

        try:
            windowClass = win32gui.RegisterClass(wndclass)  # 注册窗口类
            hwnd = win32gui.CreateWindowEx(win32con.WS_EX_LEFT,  # 实例化对象
                                           windowClass,
                                           "",
                                           0,
                                           0,
                                           0,
                                           win32con.CW_USEDEFAULT,
                                           win32con.CW_USEDEFAULT,
                                           0,
                                           0,
                                           h_inst,
                                           None)
        except Exception as e:
            logger.error("注册检测关机事件窗口错误: ", exc_info=e)

    def shutdown_event(self, _hwnd, msg, wparam, lparam):  # 关机事件后执行的函数
        if self.callback is not None:
            try:
                self.callback()
            except Exception as e:
                logger.error("运行事件回调函数错误: ", exc_info=e)

    def exit(self):
        self.running = False

    def mainloop(self):
        while self.running:
            win32gui.PumpWaitingMessages()
            sleep(0.5)
