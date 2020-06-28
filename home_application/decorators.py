# -*- coding: utf-8 -*-
import time


def calculate_func_execute_time(func):
    """计算函数的运行时间"""
    def wrapper(*args, **kwargs):
        start = time.time()
        tmp_f = func(*args, **kwargs)
        end = time.time()
        print("{func}()的运行时间为: {execute_time}ms".format(
            func=func.__name__,
            execute_time=1000 * (end-start)))
        return tmp_f
    return wrapper
