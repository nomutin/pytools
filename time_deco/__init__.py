from functools import wraps
import time

def time_deco(func) :
    @wraps(func)
    def wrapper(*args, **kargs) :
        start = time.time()
        ret = func(*args,**kargs)
        print('モジュール名：{0}\n実行時間：{1}\n'.format(func.__name__,time.time()-start))
        return ret
    return wrapper
