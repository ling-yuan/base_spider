from copy import deepcopy
import time
from universal_spider.tools import logger


def retry_wapper(times=5, delay=1):
    """
    重试装饰器

    :param func: 函数
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            i = 0
            while (i := i + 1) <= times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger(func.__name__).error(f"第{i}次执行失败: {e}")
                    time.sleep(delay)
            logger(func.__name__).error(f"执行{times}次后仍失败")
            raise Exception(f"执行{times}次后仍失败")

        return inner

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
        logger(func.__name__).info(f"执行时间: {end_time - start_time:.3f}秒")
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


def catch_wapper(func):
    """
    捕获异常装饰器，捕获异常但不抛出异常

    :param func: 函数
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger(func.__name__).error(f"捕获异常: {e}")

    return wrapper


def deepcopy_wapper(func):
    """
    深拷贝装饰器

    :param func: 函数
    """

    def wrapper(*args, **kwargs):
        args = deepcopy(args)
        kwargs = deepcopy(kwargs)
        return func(*args, **kwargs)

    return wrapper
