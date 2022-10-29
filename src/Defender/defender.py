"""
作者: 爱和牛奶的涛哥
"""
VERSION = (0, 1, 1, 20221001_092810)

# Python Wheels Import
from win32process import GetModuleFileNameEx  # 使用pid获取可执行文件位置
from win32api import OpenProcess
from win32con import PROCESS_QUERY_LIMITED_INFORMATION
from subprocess import run
from psutil import pid_exists, process_iter
from time import sleep
from sys import argv, exit
from os import getpid
from os.path import split, splitext, exists, isdir

argvs = argv[1:]
pid_self = getpid()

# My Files Import
from src.Defender.log import Logging


# End Import

class Defend:
    """
    error_code: -1 pid未传入; -2 传入的pid不是一个合法的pid; -3 超出设定最大重新打开的尝试上限;
    """

    def __init__(self, pid: int, file: str):
        print("\nWelcome to ues the Defender(Version = {}) by 爱和牛奶的涛哥\n".format(VERSION))

        self.__error_code = 0
        self.__error_info = False

        self.__pid = 0

        self.__pid = pid
        self.__file = file

        self.config = {
            "run": True,
            "killed-run": self.restart,
            "wait": 0.5,
            "max-range": 0,
            "max-pid": 0,
            "outlog": True,
        }

        self.restarted = False
        self.range = 1
        self.__find_filename = 0

        if self.config.get("outlog", False):
            p_name = splitext(split(self.file.split(" ")[0])[-1])[0] + ".exe"
            logging.write_log("In defender.py ({}) INFO: 启动成功 (file= {})".format(pid_self, p_name))

    def __exit(self):
        return self.__error_code, self.__error_info

    @property
    def pid(self):
        return self.__pid

    @property
    def file(self):
        return self.__file

    @staticmethod
    def get_filename_by_pid(pid):
        try:
            h_obj = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
            file = GetModuleFileNameEx(h_obj, 0)
        except Exception as e:
            file = None

        return file

    @staticmethod
    def get_pid_by_filename(filename):
        try:
            pids = process_iter()
            for pid in pids:
                if pid.name() == filename:
                    return pid.pid
        except Exception as e:
            pass

    def restart(self, filename):
        if filename is not None:
            filename_without_argv = filename.split(" ")[0]
            if exists(filename_without_argv) and not isdir(filename_without_argv):
                try:
                    run(f"start {filename}", shell=True)
                    return True, self.get_pid_by_filename(split(filename)[-1])
                except Exception as e:
                    return False, 0
            else:
                if self.config.get("outlog", False):
                    logging.write_log(
                        "In defender.py ({}) WARNING: 尝试打开 \"{}\" 时发现 \"{}\" 不存在或是一个文件夹无法打开".format(
                            pid_self, filename, filename))
                return False, 0
        else:
            return False, 0

    def mainloop(self):
        while self.config.get("run", True) and self.__error_code == 0:
            sleep(self.config.get("wait", 0))
            p_name = splitext(split(self.file.split(" ")[0])[-1])[0] + ".exe"

            if self.restarted:
                self.range += 1

            max_range = self.config.get("max-range", 0)
            max_pid = self.config.get("max-pid", 0)

            if self.range > max_range > 0:
                self.__error_info = "Range > MaxRange"
                self.__error_code = -3

            if self.__pid is None or self.__pid < 0:
                if self.config.get("outlog", False):
                    if self.__find_filename <= 0:
                        logging.write_log("In defender.py ({}) INFO: 尝试获取 {} 的 pid".format(pid_self, p_name))
                    else:
                        logging.write_log(
                            "In defender.py ({}) WARNING: 获取 {} 的 pid 失败, 已失败 {}/{} (<=0 未无限制)".format(
                                pid_self,
                                p_name,
                                self.__find_filename,
                                max_pid))
                self.__pid = self.get_pid_by_filename(p_name)
                if self.__pid is None:
                    self.__find_filename += 1
                    self.restart(self.file)
                    self.__pid = self.get_pid_by_filename(p_name)
                else:
                    if self.config.get("outlog", False):
                        logging.write_log(
                            "In defender.py ({}) INFO: 获取 {} 的 pid 成功".format(pid_self, p_name))
                    self.__pid = self.get_pid_by_filename(p_name)
                    self.__find_filename = 0
            elif self.__pid == 0:
                self.__error_info = "Pid Unknown"
                self.__error_code = -1
            else:
                if not pid_exists(self.pid):
                    logging.write_log(
                        "In defender.py ({}) INFO: {} ({}) 被关闭, 正在尝试打开".format(pid_self, p_name, self.pid))
                    func = self.config.get("killed-run", None)
                    if func is not None:
                        return_code: tuple = func(self.file)
                        if return_code is None or return_code[0] is False:
                            self.restarted = True
                            logging.write_log(
                                "In defender.py ({}) WARNING: {} 打开失败, 已尝试 {}/{} (<=0 未无限制)".format(
                                    pid_self,
                                    p_name,
                                    self.range,
                                    max_range + 1))
                        else:
                            self.__pid = return_code[1]
                            self.restarted = False
                            self.range = 1
                            logging.write_log(
                                "In defender.py ({}) INFO: {} 打开成功".format(pid_self, p_name))

            if self.__find_filename > max_pid > 0:
                self.__error_code = -1
                self.__error_info = "Pid 获取屡次失败, 注意explorer等系统进程无法获取!"

        return self.__error_code, self.__error_info


logging = Logging()
logging.log_file = "../log/$(now_time)$.defend.log"
logging.write_log(None)

if __name__ == "__main__":

    __error_info = f"Unknown"
    __error_code = -3
    __pid = None
    try:
        __pid = int(argvs[0])
        __error_info = f""
        __error_code = 0
    except ValueError:
        __error_info = f"Pid 不合法"
        __error_code = -2
    except IndexError:
        __error_info = f"Pid 未传入"
        __error_code = -1

    if __pid is None:
        logging.write_log("In defender.py ({}) ERROR: error_code: {} error_info: {} 已退出".format(
            pid_self,
            __error_code,
            __error_info))

    __error_info = f"Unknown"
    __error_code = -3
    __file = None
    try:
        __file = argvs[1]
        __error_info = f""
        __error_code = 0
    except IndexError:
        __error_info = f"File 未传入"
        __error_code = -1

    if __file is None:
        logging.write_log("In defender.py ({}) ERROR: error_code: {} error_info: {} 已退出".format(
            pid_self,
            __error_code,
            __error_info))
        exit(__error_code)

    defend = Defend(__pid, __file)
    res = defend.mainloop()

    logging.write_log(
        "In defender.py ({}) ERROR: error_code: {} error_info: {} 已退出并重启此程序".format(pid_self, *res))
    run(f"start {argv[0]} {__pid} {__file}", shell=True)  # 自动启动, 打包前请解除注释
