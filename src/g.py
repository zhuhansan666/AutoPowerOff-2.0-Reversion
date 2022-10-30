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

check = Check(information)

file_tools.create_file(app_config.log_filename)
logging.basicConfig(level=information.config["debug"]["log-level"], style='{', encoding="u8",
                    filename=app_config.log_filename,
                    format='[{asctime}:%03d] [{levelname}] In {filename} Line {lineno}: {message}' % (
                                   time() % 1 * 1000),
                    datefmt='%Y-%m-%d %H:%M:%S')

VERSION = app_config.VERSION

