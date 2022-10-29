from src.check import Check
from src.g import information

from time import time as get_time
from time import sleep


class BackGround:
    def __init__(self, check_obj: Check):
        self.__check = check_obj

        self.running = True

    def mainloop(self):
        while self.running:
            if information.check is not False:
                ...
