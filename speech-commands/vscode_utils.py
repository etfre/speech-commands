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


clip = {
    "cut": Key(f"{CMD_OR_CTRL}-x"),
    "copy": Key(f"{CMD_OR_CTRL}-c") + Key("escape"),
    "take": None,
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
