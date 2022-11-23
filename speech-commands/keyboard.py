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
    "slash": "/",
    "backslash": "\\",
    "addition": "+",
    "downscore": "_",
    "asterisk": "*",
    "colon": ":",
    "comma": ",",
    "(semicolon|semi colon)": ";",
    "at sign": "@",
    "double": '"',
    "single": "'",
    "number sign": "#",
    "dollar": "$",
    "percent": "%",
    "ampersand": "&",
    "(equal|equals)": "=",
    "addition": "+",
    "space": " ",
    "exclamation": "!",
    "question": "?",
    "squiggle": "~",
    "backtick": "`",
    "caret": "^",
    "tab key": "\t",
    "open brace": "{",
    "open bracket": "[",
    "open pen": "(",
    "open angle": "<",
    "close brace": "}",
    "close bracket": "]",
    "close pen": ")",
    "close angle": ">",
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
    "alpha": "a",
    "bravo ": "b",
    "charlie ": "c",
    "danger ": "d",
    "eureka ": "e",
    "foxtrot ": "f",
    "gorilla ": "g",
    "hotel ": "h",
    "india ": "i",
    "juliet ": "j",
    "kilo ": "k",
    "lima ": "l",
    "michael ": "m",
    "november ": "n",
    "oscar ": "o",
    "papa ": "p",
    "quiet ": "q",
    "romeo ": "r",
    "sierra ": "s",
    "tango ": "t",
    "uniform ": "u",
    "victor ": "v",
    "whiskey ": "w",
    "x-ray ": "x",
    "yankee ": "y",
    "zulu ": "z",
}

keys = {
    "north": "up",
    "south": "down",
    "west": "left",
    "east": "right",
    "page up": "pgup",
    "page down": "pgdown",
    "(home key|first)": "home",
    "(end key|final)": "end",
    "enter": "enter",
    "escape": "escape",
    "delete": "del",
    "snipe": "backspace",
}

digits = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
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

# # generate uppercase versions of every letter
# upperLetterMap = {}
# for letter in letterMap:
#     upperLetterMap["upper " + letter] = letterMap[letter].upper()
# letterMap.update(upperLetterMap)


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

    "upper <letters>": Function(lambda **kw: Text(kw["letters"].upper()).execute()),
    "<all_chars>": "%(all_chars)s",
    "<modifierSingle> <all_chars>": "{%(modifierSingle)s:down}%(all_chars)s{%(modifierSingle)s:up}",
    "<modifier1> <modifier2> <all_chars>": Key("%(modifier1)s:down") + Key("%(modifier2)s:down") + Text("%(all_chars)s") + Key("%(modifier2)s:up") + Key("%(modifier1)s:down") ,
    "<keys>": "{%(keys)s}",
    "<modifierSingle> <keys>": "{%(modifierSingle)s:down}{%(keys)s}{%(modifierSingle)s:up}",
    "<modifier1> <modifier2> <keys>": Key("%(modifier1)s:down") + Key("%(modifier2)s:down") + Key("%(keys)s") + Key("%(modifier2)s:up") + Key("%(modifier1)s:down") ,
    "parentheses": Text("()"),
    "brackets": Text("[]"),
    "braces": Text("{}"),
    "(space | spaces) around": Text("  ") + Key("left"),
    "jump left": Key("c-left"),
    "jump right": Key("c-right"),
    "hexadecimal": Text("0x"),
    "number <num>": Text("%(num)s"),
    "<operators>": " %(operators)s ",
    "short <operators>": "%(operators)s",
}

if utils.IS_MAC:
    grammarCfg['undo'] = Key("w-z")
    grammarCfg['redo'] = Key("ws-z")
else:
    grammarCfg['undo'] = Key("c-z")
    grammarCfg['redo'] = Key("c-y")


extras = [
    Dictation("text"),
    Dictation("text2"),
    Choice("char", specialCharMap),
    Choice("letters", letterMap),
    Choice("all_chars", all_chars),
    Choice("keys", keys),
    Choice('digits', digits),
    Choice("modifier1", singleModifierMap),
    Choice("modifier2", singleModifierMap),
    Choice("modifierSingle", singleModifierMap),
    Choice("operators", operators),
    utils.num,
]

utils.load_commands(None, repeat_commands=grammarCfg, extras=extras)
