from src.load import Load
from src.g import *

from time import sleep


def init():
    load = Load()
    load.reload()


if __name__ == '__main__':
    init()
    print(f"{information.config}")
