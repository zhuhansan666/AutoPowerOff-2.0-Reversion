from src.information import *
from src.config import Config
from src.app_config import AppConfig
from src.check import Check

from Tools import FileTools

from load import Load

from time import time
import logging


file_tools = FileTools()
app_config = AppConfig()
config = Config(app_config.config_file)
information = Information()
events_information = EventsInformation()

load = Load(information, app_config, config)
load.reload()

check = Check(information, events_information)

file_tools.create_file(app_config.log_filename)
logging.basicConfig(level=information.config.get("debug", app_config.default_debug)["log-level"], style='{',
                    encoding="u8", filename=app_config.log_filename if information.config.get(
                        "debug", app_config.default_debug)["out-log"] else None,
                    format='[{asctime}:%03d] [{levelname}] In {filename} At PID-{process}'
                           '.{threadName} Line {lineno}: {message}' % (
                                   time() % 1 * 1000),
                    datefmt='%Y-%m-%d %H:%M:%S')

VERSION = app_config.VERSION

logger = logging.getLogger("g")
version = [str(item) for item in VERSION]
logger.info("\n" + "-" * 100 + "\n" + "欢迎使用 由 爱喝牛奶の涛哥 和 CYH 共同制作的 AutoPowerOff2.0 ({})".format(
    ".".join(version)) + "\n" + "-" * 100
            )
