from src.g import *
from src.startup import set_startup
from src.background import BackGround
from src.Tools import Tools
from src.get_shutdown import ShutdownEvent
from src.ui_init import *

import atexit

from threading import Thread
from logging import getLogger

logger = getLogger("main")
from time import sleep, time
from sys import argv
from os import path, chdir

tools = Tools()
chdir(tools.get_current_path())

result = set_startup("AutoPowerOff2", '\"{}\"'.format(path.abspath(argv[0])))
if result[0] != 0:
    logger.error(f"写入自启动发生错误: {result[-1]}")


def shutdown_event_func():
    logger.info("检测到关机系统事件, 已退出")
    events_information.exit = True


def all_exit():
    background.exit()
    check.exit()
    shutdown_event.exit()


@atexit.register
def exit_func():
    _version = [str(item) for item in VERSION]
    logger.info("感谢使用 由 爱喝牛奶の涛哥 和 CYH 共同制作的 AutoPowerOff2.0 ({}), Github开源地址: {}".format(
        ".".join(_version),
        app_config.github_url
    ))


try:
    shutdown_event = ShutdownEvent(shutdown_event_func)

    background = BackGround(check, events_information, load, app_config)
    background_thread = Thread(target=background.mainloop, daemon=True)
    background_thread.start()
    # background.running

    while True:
        sleep(1)
        print(time() - check.latest_keyboard_mouse_event_time)
        if events_information.exit:
            all_exit()
            break
except Exception as e:
    information.global_error = e
    events_information.exit = True
    logger.error("主程序发生错误: ", exc_info=e)
