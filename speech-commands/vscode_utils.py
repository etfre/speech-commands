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
