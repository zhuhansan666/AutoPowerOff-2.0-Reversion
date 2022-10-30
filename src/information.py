class Information:
    def __init__(self):
        self.__config = {}
        self.global_error = RuntimeError("未获取到ERROR")

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, value: dict):
        self.__config = value


class EventsInformation:
    def __init__(self):
        self.check: bool = False

        # 0 -> 无, 1 -> 到达时间并在设定时间内无操作, 2 -> 全屏应用程序关闭后设定短时间内无操作, 3 -> 到达强制关机时间
        self.shutdown_type = 0

        # 关机内容, 如到达时间、全屏应用程序关闭、到达强制关机时间等
        self.shutdown_info = ""

        self.exit = False
