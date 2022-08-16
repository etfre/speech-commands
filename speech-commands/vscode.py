import time
import utils
import contexts
from dragonfly import *
from breathe import Breathe
from srabuilder.actions import surround, between
from srabuilder import rules

clip = {
    "cut": "cut",
    "copy": "copy",
    "select": "(select)",
}
clip_action = {
    "cut": Key("c-x"),
    "copy": Key("c-c") + Key("escape"),
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
    "all": Key("c-a"),
}

select_actions_multiple = {
    "line": Key("c-l"),
    "word": Key("c-d"),
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

git_commands = {
    "git push": "{f1}git push",
    "git stash": "{f1}git stash",
    "git pop stash": "{f1}git pop latest stash",
    "git commit": "{f1}git commit",
    "git commit all": "{f1}git commit all",
    "git stage [changes]": "{f1}git stage",
    "git stage all [changes]": "{f1}git stage all changes",
    "git unstage [changes]": "{f1}git unstage",
    "git unstage all [changes]": "{f1}git unstage all changes",
    "git create branch": "{f1}git create branch",
    "git custom create branch ": "{f1}git create branch from",
    "git open changes ": "{f1}git open changes",
    "git discard changes ": "{f1}git discard changes",
}

non_repeat_mapping = {
    "<clip> <movements>": Function(clip_move),
    "[<n>] <clip> <movements_multiple>": Function(clip_move),
    "[<n>] <clip> <select_actions_multiple>": Function(do_select),
    "select content": "{home}{s-end}",
    "copy content": "{home}{s-end}{c-c}{escape}",
    "cut content": "{home}{s-end}{c-v}",
    "delete content": "{home}{s-end}{backspace}",
    "<clip> <select_actions_single>": Function(do_select),
    "file explorer": "{cs-e}",
    "source control": "{cs-g}g",
    "command palette": "{f1}",
    "rename": "{f2}",
    "go to definition": "{f12}",
    "comment": "{c-slash}",
    "block comment": "{as-a}",
    "fuzzy": "{c-p}",
    "save file": "{c-s}",
    "open recent": "{c-r}",
    "shark": "{c-enter}{c-[}",
    "(search file) | (file search)": "{c-f}",
    "(search project) | (project search)": "{cs-f}",
    "(replace [in] file) | (file replace)": "{c-h}",
    "(replace [in] project) | (project replace)": "{cs-h}",
    "surround parentheses": surround("(", ")"),
    "surround blocks": surround("[", "]"),
    "surround single": surround("'", "'"),
    "surround double": surround('"', '"'),
    "call that": "(){left}",
    "new tab": "{c-n}",
    "go to line <n>": between(Key("c-g"), Function(lambda **k: Text(str(k["n"])).execute()), Key('enter')),
    "below line <n>": between(Key("c-g"), Function(lambda **k: Text(str(k["n"])).execute()), Key('enter'), Key('c-enter')),
    "go to line": "{c-g}",
    "split editor": "{c-backslash}",
    "close editor": "{c-f4}",
    **git_commands
}

if utils.IS_MAC:
    non_repeat_mapping['fuzzy'] = "{w-p}"

repeat_mapping = {
    "flip north": "{a-up}", 
    "flip south": "{a-down}",
    "duplicate north": "{as-up}",
    "duplicate south": "{as-down}",
    "cursor north": "{ca-up}",
    "cursor south": "{ca-down}",
    "tab left": "{c-pageup}",
    "tab right": "{c-pagedown}",
    "new line": "{c-enter}",
    "new line above": "{cs-enter}",
    "out dent": "{c-[}",
    "indent": "{c-]}",
    "close tab": "{c-w}",
    "grab": "{c-d}",
    "expand": "{as-right}",
    "shrink": "{as-left}",
    "previous editor": "{c-k}{c-left}",
    "next editor": "{c-k}{c-right}",
    "move editor right": "{c-k}{left}",
    "move editor left": "{c-k}{right}",
}

utils.load_commands(
    contexts.vscode,
    commands=non_repeat_mapping,
    extras=[
        Choice("clip", clip),
        Choice("movements_multiple", movements_multiple),
        Choice("select_actions_multiple", select_actions_multiple),
        Choice("movements", movements),
        Choice("select_actions_single", select_actions_single),
    ]
)
utils.load_commands(contexts.vscode, repeat_commands=repeat_mapping)