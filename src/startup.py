from traceback import format_exc
from src.Tools import FileTools

file_tools = FileTools()

import winreg


def set_startup(key_name: str = "_", target_file: str = None, _type: str | tuple = "system"):
    """
        写入自启动
    """
    _type_lower = _type.lower()
    if _type_lower == "sys" or _type_lower == "system":
        reg_path = (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
    elif _type_lower == "user" or _type_lower == "usr":
        reg_path = (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
    else:
        if type(_type) != tuple:
            return -1, "_type 不合法"
        else:
            reg_path = _type

    if target_file is None:
        return -2, "target_file does not be \"None\""
    else:
        if file_tools.is_true_path(target_file):
            try:
                with winreg.OpenKeyEx(*reg_path, access=winreg.KEY_ALL_ACCESS) as reg:
                    winreg.SetValueEx(reg, key_name, 0, winreg.REG_SZ, target_file)
                error = ""
            except Exception as e:
                error = e

            if type(error) != str:
                return -3, error
            else:
                return 0, error
        else:
            return -2, "target_file path is not true"
