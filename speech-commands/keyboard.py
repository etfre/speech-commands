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

import utils

try:
    from dragonfly.actions.keyboard import keyboard
    from dragonfly.actions.typeables import typeables

    if "semicolon" not in typeables:
        typeables["semicolon"] = keyboard.get_typeable(char=";")
except:
    pass

from srabuilder import rules


release = Key("shift:up, ctrl:up, alt:up")


# For repeating of characters.
specialCharMap = {
    "(Vertical)": "|",
    "(dash)": "-",
    "period": ".",
    "comma": ",",
    "backslash": "\\",
    "downscore": "_",
    "asterisk": "*",
    "colon": ":",
    "(semicolon|semi colon)": ";",
    "at sign": "@",
    "[double] quote": '"',
    "single quote": "'",
    "number sign": "#",
    "dollar": "$",
    "percent": "%",
    "ampersand": "&",
    "slash": "/",
    "(equal|equals)": "=",
    "addition": "+",
    "space": " ",
    "exclamation": "!",
    "question": "?",
    "caret": "^",
    "north": "up",
    "south": "down",
    "west": "left",
    "east": "right",
    "page up": "pgup",
    "page down": "pgdown",
    "(home key|first)": "home",
    "(end key|final)": "end",
    "space": "space",
    "enter": "enter",
    "tab key": "tab",
}

# Modifiers for the press-command.
modifierMap = {
    "alt": "a",
    "angry": "a",
    "control": "c",
    "shift": "shift",
    "super": "w",
}

# Modifiers for the press-command, if only the modifier is pressed.
singleModifierMap = {
    "alt": "alt",
    "angry": "alt",
    "control": "ctrl",
    "shift": "shift",
    "super": "win",
}

letterMap = {
    "air": "a",
    "bat": "b",
    "cap": "c",
    "drink": "d",
    "each": "e",
    "fine": "f",
    "gust": "g",
    "harp": "h",
    "sit": "i",
    "jury": "j",
    "kilo": "k",
    "look": "l",
    "made": "m",
    "near": "n",
    "odd": "o",
    "pit": "p",
    "quench": "q",
    "red": "r",
    "sun": "s",
    "trap": "t",
    "urge": "u",
    "vest": "v",
    "whale": "w",
    "plex": "x",
    "yank": "y",
    "zip": "z",
}

all_chars = {**letterMap, **specialCharMap}

operators = {
    "plus": "+",
    "minus": "-",
    "times": "*",
    "divide": "/",
    "floor divide": "//",
    "modulo": "%",
    "greater than": ">",
    "less than": "<",
}

# generate uppercase versions of every letter
upperLetterMap = {}
for letter in letterMap:
    upperLetterMap["upper " + letter] = letterMap[letter].upper()
letterMap.update(upperLetterMap)


grammarCfg = {
    # Navigation keys.
    "application key": release + Key("apps/3"),
    "win key": release + Key("win/3"),
    "copy that": release + Key("c-c"),
    "cut that": release + Key("c-x"),
    "paste that": release + Key("c-v"),
    "(hold|press) alt": Key("alt:down/3"),
    "release alt": Key("alt:up"),
    "(hold|press) shift": Key("shift:down/3"),
    "release shift": Key("shift:up"),
    "(hold|press) control": Key("ctrl:down/3"),
    "release control": Key("ctrl:up"),
    "release [all]": release,
    "single": "{squote}",
    "double": Key("dquote"),
    "squiggle": Text("~"),
    "backtick": Key("backtick"),
    "colon": Key("colon"),
    "(semicolon|semi colon)": ";",
    "comma": Key("comma"),
    "dash": Key("hyphen"),
    "downscore": Key("underscore"),
    "<letters>": Text("%(letters)s"),
    "<char>": Key("%(char)s"),
    "<modifierSingle> <all_chars>": "{%(modifierSingle)s:down}{%(all_chars)s}{%(modifierSingle)s:up}",
    "<modifier1> <modifier2> <all_chars>": Key("%(modifier1)s:down") + Key("%(modifier2)s:down") + Key("%(all_chars)s") + Key("%(modifier2)s:up") + Key("%(modifier1)s:down") ,
    "open brace": Key("lbrace"),
    "open bracket": Key("lbracket"),
    "open pen": "(",
    "close brace": Key("rbrace"),
    "close bracket": Key("rbracket"),
    "close pen": Key("rparen"),
    "parentheses": Text("()"),
    "brackets": Text("[]"),
    "braces": Text("{}"),
    "escape": Key("escape"),
    "comma": Key("comma"),
    "home key": Key("home"),
    "end key": Key("end"),
    "delete": Key("del"),
    "snipe ": Key("backspace"),
    "before": Key("c-left"),
    "after": Key("c-right"),
    "hexadecimal": Text("0x"),
    "undo": Key("c-z"),
    "redo": Key("c-y"),
    "number <digits>": Text("%(digits)s"),
    "<operators>": " %(operators)s ",
    "short <operators>": "%(operators)s",
}

extras = [
    Dictation("text"),
    Dictation("text2"),
    Choice("char", specialCharMap),
    Choice("letters", letterMap),
    Choice("all_chars", all_chars),
    rules.digits,
    Choice("modifier1", singleModifierMap),
    Choice("modifier2", singleModifierMap),
    Choice("modifierSingle", singleModifierMap),
    Choice("operators", operators),
]

utils.load_commands(None, repeat_commands=grammarCfg, extras=extras)
