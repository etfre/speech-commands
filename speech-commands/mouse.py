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

from srabuilder import rules

grammarCfg = Config("multi edit")
grammarCfg.cmd = Section("Language section")
grammarCfg.cmd.map = Item(
    {
        "(mouse | left) click": Mouse("left"),
        "(mouse | left) hold": Mouse("left:down"),
        "(mouse | left) release": Mouse("left:up"),
        "right hold": Mouse("left:down"),
        "right release": Mouse("left:up"),
        "double click": Mouse("left:2"),
        "right click": Mouse("right"),
        "mouse up": Function(lambda **kw: Mouse(f"<0, {kw['n'] * -5}>").execute()),
        "mouse right": Function(lambda **kw: Mouse(f"<{kw['n'] * 5}, 0>").execute()),
        "mouse down": Function(lambda **kw: Mouse(f"<0, {kw['n'] * 5}>").execute()),
        "mouse left": Function(lambda **kw: Mouse(f"<{kw['n'] * -5}, 0>").execute()),
    },
    namespace={
        "Key": Key,
        "Text": Text,
    },
)


class MouseRule(MappingRule):
    exported = False
    mapping = grammarCfg.cmd.map
    extras = [
        rules.num,
    ]
    defaults = {
        "n": 1,
    }


def root_rule():
    return MouseRule(name="mouse")