import threading, time

_lock = threading.Lock()
_events = []


def emit(kind, **data):
    with _lock:
        _events.append({"kind": kind, "t": time.time(), **data})


def since(i):
    with _lock:
        return _events[i:]


def last_reset():
    """Index of the most recent 'reset' event, so new browsers skip old runs."""
    with _lock:
        for i in range(len(_events) - 1, -1, -1):
            if _events[i]["kind"] == "reset":
                return i
        return 0
