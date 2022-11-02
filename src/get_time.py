"""
    获取UTC-8时间戳
"""
from requests import get
from src.app_config import AppConfig

app_config = AppConfig()


def get_time():
    try:
        result = float(get(app_config.get_time_url[0], headers=app_config.ua).text)
        if app_config.get_time_url[1].lower() == "ms":
            result = result / 1000
        return 0, result
    except Exception as e:
        return -1, e
