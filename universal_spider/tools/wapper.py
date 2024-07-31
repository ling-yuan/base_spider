import time
from universal_spider.tools import logger


def retry_wapper(func):
    """
    重试装饰器

    :param func: 函数
    """

    def wrapper(*args, **kwargs):
        for i in range(5):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger(func.__name__).error(f"第{i + 1}次执行失败: {e}")
        logger(func.__name__).error("执行5次失败")
        raise Exception("执行5次失败")

    return wrapper


def time_wapper(func):
    """
    计时装饰器

    :param func: 函数
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger(func.__name__).info(f"执行时间: {end_time - start_time}秒")
        return result

    return wrapper


def run_now_wapper(func):
    """
    立即执行被装饰的函数一次，并保持原函数正常调用
    注意：被装饰函数所需的参数必须都含有默认值，否则则会产生异常

    :param func: 函数
    """
    try:
        func()
    except Exception as e:
        logger(func.__name__).error(f"立即执行失败: {e}")
        raise e
    return func
