import signal

import multiprocess as mp

from typing import Tuple

timed_out = 10

def _check(code: str, queue: mp.Queue):
    # Set time limit: 10 seconds
    signal.alarm(timed_out)

    def _timelimit(signalnum, frame):
        raise TimeoutError("timed out")
    
    signal.signal(signal.SIGALRM, _timelimit)

    try:
        exec(code)
        queue.put((True, "pass"))

    # If any exception occurs in this execution
    except Exception as e:
        queue.put((False, e))

def run_code(task_id: str, code: str) -> Tuple[str, Tuple[bool, str]]:
    queue = mp.Queue()
    proc = mp.Process(target=_check, args=(code, queue))
    proc.start()

    proc.join(timed_out + 1)
    stat = queue.get() if not queue.empty() else (False, "unknown error")
    proc.terminate()

    return task_id, stat
