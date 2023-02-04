import threading
import queue
import time
import dragonfly as df

_action_queue = queue.Queue()

def _drain_queue(q: queue.Queue):
    vals = []
    while True:
        try:
            vals.append(q.get_nowait())
        except queue.Empty:
            break
    return vals

def _scroll_worker():
    while True:
        action, interval = _action_queue.get()
        while True:
            queued_actions = _drain_queue(_action_queue)
            if queued_actions:
                action, interval = queued_actions[-1]
            elif interval:
                time.sleep(interval)
            if action is None:
                break
            action.execute()

def scroll(directions, interval=0.01):
    x, y = directions
    action = df.Mouse(f'<{x}, {y}>')
    _action_queue.put((action, interval))

def stop():
    _action_queue.put((None, None))

threading.Thread(target=_scroll_worker, daemon=True).start()