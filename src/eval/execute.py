import signal

import multiprocessing as mp

from typing import Tuple

timed_out = 10

def _check(code: str, order: int, queue: mp.Queue):
    # Set time limit: 10 seconds
    signal.alarm(timed_out)

    def _timelimit(signalnum, frame):
        raise TimeoutError("timed out")
    
    signal.signal(signal.SIGALRM, _timelimit)

    # namespace
    ns = {}
    try:
        exec(code, ns)
        queue.put((True, "pass"))

    # If any exception occurs in this execution
    except Exception as e:
        queue.put((False, str(e)))

    #if order == 55:
    #    print(ns)

def run_code(order: int, code: str) -> Tuple[str, Tuple[bool, str]]:
    queue = mp.Queue()
    proc = mp.Process(target=_check, args=(code, order, queue))
    proc.start()

    proc.join(timed_out + 1)
    stat = queue.get() if not queue.empty() else (False, "unknown error")
    proc.terminate()

    return order, stat
