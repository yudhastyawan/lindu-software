import time

_start_time = time.time()

def tic():
    global _start_time
    _start_time = time.time()

def tac():
    t_sec = round(time.time() - _start_time)
    (t_min, t_sec) = divmod(t_sec,60)
    (t_hour,t_min) = divmod(t_min,60)
    elt = '{}hour:{}min:{}sec'.format(t_hour,t_min,t_sec)
    return elt