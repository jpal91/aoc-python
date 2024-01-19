import time


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, format((end - start) * 1000, '.3f'), 'ms')
        return res
    return wrapper