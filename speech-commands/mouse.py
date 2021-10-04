# Low-level keyboard input module
#
# Based on the work done by the creators of the Dictation Toolbox
# https://github.com/dictation-toolbox/dragonfly-scripts
#
# and _multiedit-en.py found at:
# http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/mod-_multiedit.html
#
# Modifications by: Tony Grosinger
#
# Licensed under LGPL

from dragonfly import *

try:
    from dragonfly.actions.keyboard import keyboard
    from dragonfly.actions.typeables import typeables

    if "semicolon" not in typeables:
        typeables["semicolon"] = keyboard.get_typeable(char=";")
except:
    pass

from srabuilder.actions import scroll
import utils

scroll_directions = {
    'up': (0, -1),
    'main': (1, -1),
    'right': (1, 0),
    'floor': (1, 1),
    'down': (0, 1),
    'air': (-1, 1),
    'left': (-1, 0),
    'wash': (-1, -1),
}

def mouse_move(direction, n):
    multiplier = 5
    x, y = direction[0] * n, direction[1] * n
    Mouse(f'<{x}, {y}>').execute()

def scroll_function(direction, multiplier=1, drag=False):
    direction = [x * multiplier for x in direction]
    if drag:
        Mouse('left:down').execute()
    scroll.scroll(direction)

def stop_scroll():
    scroll.stop()
    Mouse('left:up').execute()

commands = {
    "[<positive_digit>] scroll <scroll_directions>": Function(lambda **kw: scroll_function(kw['scroll_directions'], multiplier=kw['positive_digit'])),
    "[<positive_digit>] drag <scroll_directions>": Function(lambda **kw: scroll_function(kw['scroll_directions'], multiplier=kw['positive_digit'], drag=True)),
    "stop": Function(stop_scroll),
    "(mouse | left) click": Mouse("left"),
    "(mouse | left) hold": Mouse("left:down"),
    "(mouse | left) release": Mouse("left:up"),
    "right hold": Mouse("right:down"),
    "right release": Mouse("right:up"),
    "double click": Mouse("left:2"),
    "right click": Mouse("right"),
    "[<n>] mouse <scroll_directions>": Function(lambda **kw: mouse_move(kw['scroll_directions'], kw['n'])),
}

extras = [Choice('scroll_directions', scroll_directions), utils.positive_digit]
utils.load_commands(None, commands=commands, extras=extras)