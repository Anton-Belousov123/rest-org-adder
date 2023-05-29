
import time


def timer(f):
    def tmp(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print(f"Время выполнения функции  {f.__name__}: %f" % (time.time() - t))
        return res

    return tmp
