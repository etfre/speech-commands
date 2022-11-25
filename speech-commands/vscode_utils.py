import time
import os
import re
import utils
from dragonfly import *
from srabuilder import rules, clipboard

IS_MAC = utils.IS_MAC
CMD_OR_CTRL = "w" if IS_MAC else "c"

EXPAND_COMMAND = Key("as-right")
SHRINK_COMMAND = Key("as-left")
COPY_COMMAND = Key(f"{CMD_OR_CTRL}-c")
EXPAND_AND_COPY = EXPAND_COMMAND + COPY_COMMAND


def expand_while(first_check=None, last_check=None, on_done=None):
    assert first_check or last_check

    def do_check(check, to_check: str):
        if isinstance(check, (list, tuple)):
            return any(do_check(x, to_check) for x in check)
        if isinstance(check, str):
            return to_check.lstrip().startswith(check)
        elif isinstance(check, re.Pattern):
            return bool(check.search(to_check.strip()))
        elif callable(check):
            return check(to_check)
        else:
            raise TypeError

    expand_count = 0
    is_match = False
    prev = None
    curr: str = clipboard.get() or ""
    with clipboard.save_current():
        while prev is None or prev != curr:
            EXPAND_AND_COPY.execute()
            expand_count += 1
            time.sleep(0.1)
            prev, curr = curr, clipboard.get()
            if curr:
                spl = curr.split(os.linesep)
                first, last = spl[0], spl[-1]
                first_match = True if first_check is None else do_check(first_check, first)
                last_match = True if last_check is None else do_check(last_check, last)
                is_match = first_match and last_match
            else:
                is_match = False
            if is_match:
                break
    if is_match:
        if on_done:
            if isinstance(on_done, ActionBase):
                on_done.execute()
            elif callable(on_done):
                on_done()
    else:
        for i in range(expand_count):
            SHRINK_COMMAND.execute()


clip = {
    "cut": Key(f"{CMD_OR_CTRL}-x"),
    "copy": Key(f"{CMD_OR_CTRL}-c") + Key("escape"),
    "select": None,
}
clip_action = {
    "cut": Key(f"{CMD_OR_CTRL}-x"),
    "copy": Key(f"{CMD_OR_CTRL}-c") + Key("escape"),
}

movements = {
    "final": "end",
    "first": "home",
}
movements_multiple = {
    "north": "up",
    "east": "right",
    "south": "down",
    "west": "left",
}

select_actions_single = {
    "all": Key(f"{CMD_OR_CTRL}-a"),
}

select_actions_multiple = {
    "line": Key(f"{CMD_OR_CTRL}-l"),
    "word": Key(f"{CMD_OR_CTRL}-d"),
}


def clip_move(**kw):
    clip = kw["clip"]
    move = kw.get("movements_multiple") or kw.get("movements")
    move_key = Key(move) * Repeat(count=kw["n"])
    Key("shift:down").execute()
    move_key.execute()
    Key("shift:up").execute()
    if clip in clip_action:
        time.sleep(0.2)
        clip_action[clip].execute()


def do_select(**kw):
    move = kw.get("select_actions_multiple") or kw.get("select_actions_single")
    move_key = move * Repeat(count=kw["n"])
    move_key.execute()
    clip = kw["clip"]
    if clip in clip_action:
        time.sleep(0.2)
        clip_action[clip].execute()
