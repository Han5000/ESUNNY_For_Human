import functools
from threading import Thread
import arrow as ar
from time import sleep


def timeout(timeout_):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, timeout_))]

            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e

            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(timeout_)
            except Exception as je:
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret

        return wrapper

    return deco


def trade_time():
    close_time = 6
    open_time = 7
    now = ar.now()
    if now.hour == close_time:
        target = now.replace(hour=open_time).floor('hour')
        diff = target.float_timestamp - now.float_timestamp
        print('休眠', diff)
        sleep(diff)

    now = ar.now()
    if now.isoweekday() == 6:
        target = now.shift(days=2).replace(hour=open_time).floor('hour')
        diff = target.float_timestamp - now.float_timestamp
        print('休眠', diff)
        sleep(diff)

    now = ar.now()
    if now.isoweekday() == 7:
        target = now.shift(days=1).replace(hour=open_time).floor('hour')
        diff = target.float_timestamp - now.float_timestamp
        print('休眠', diff)
        sleep(diff)

