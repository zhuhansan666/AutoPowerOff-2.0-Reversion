import win32api, win32con, win32print, win32gui
from typing import Iterator


def get_task_bar_size():
    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0)))
    monitor_area = monitor_info.get("Monitor")
    work_area = monitor_info.get("Work")
    scaling = get_scaling()
    return round(work_area[2] * scaling), round((monitor_area[3] - work_area[3]) * scaling)


def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    wide = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    high = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return wide, high


def get_screen_size():
    """获取缩放后的分辨率"""
    wide = win32api.GetSystemMetrics(0)
    high = win32api.GetSystemMetrics(1)
    return wide, high


def get_scaling():
    """获取屏幕的缩放比例"""
    real_resolution = get_real_resolution()
    screen_size = get_screen_size()
    return round(real_resolution[0] / screen_size[0], 2)


def check_winsize(win_size: list | tuple, target: list | tuple):
    """检查win大小, 若前者大于或者return True"""
    if win_size[0] - target[0] >= 0 and win_size[1] - target[1] >= 0:
        return True
    return False
