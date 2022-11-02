from src.g import *
from src.startup import set_startup
from src.background import BackGround
from src.Tools import Tools
from src.get_shutdown import ShutdownEvent
from src.ui_init import *

import atexit

from traceback import format_exception
from threading import Thread
from logging import getLogger

logger = getLogger("mainloop")
from time import sleep, time
from sys import argv, excepthook
from os import path, chdir

tools = Tools()
chdir(tools.get_current_path())


class Main:

    def __init__(self):
        self.running = True

        self.background = BackGround(self.all_exit, check, events_information, load, app_config, information)
        self.shutdown_event = ShutdownEvent(self.shutdown_event_func)

        self.background_thread = Thread(name="background", target=self.background.mainloop, daemon=True)
        self.background_thread.start()

        self.write_startup()

    @staticmethod
    def write_startup():
        result = set_startup("AutoPowerOff2", '\"{}\"'.format(path.abspath(argv[0])))
        if result[0] != 0:
            logger.error(f"写入自启动发生错误: {result[-1]}")

    def shutdown_event_func(self):
        self.write_startup()
        logger.info("检测到关机系统事件, 已退出")
        events_information.exit = True

    def exit_func(self):
        self.write_startup()
        _version = [str(item) for item in VERSION]
        logger.info("感谢使用 由 爱喝牛奶の涛哥 和 CYH 共同制作的 AutoPowerOff2.0 ({}), Github开源地址: {}".format(
            ".".join(_version),
            app_config.github_url
        ))

    def all_exit(self):
        self.background.exit()
        check.exit()
        self.shutdown_event.exit()
        self.exit()

    def exit(self):
        self.running = False

    @staticmethod
    def excepthook(exc_type, exc_value, tb):
        information.global_error = tb
        events_information.exit = True
        logger.error("主程序发生错误: {}".format(format_exception(exc_type, exc_value, tb)))

    def mainloop(self):
        while self.running:
            sleep(1)
            # print(time() - check.latest_keyboard_mouse_event_time)
            if events_information.exit:
                break


if __name__ == '__main__':
    main = Main()
    excepthook = main.excepthook
    atexit.register(main.exit_func)
    main.mainloop()
