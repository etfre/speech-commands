import time
import utils
import contexts
from dragonfly import *
from breathe import Breathe
from srabuilder.actions import between
import vscode_utils

IS_MAC = utils.IS_MAC
CMD_OR_CTRL = "w" if IS_MAC else "c"

git_commands = {
    "git push": "{f1}git push",
    "git stash": "{f1}git stash",
    "git pop stash": "{f1}git pop latest stash",
    "git commit": "{f1}git commit",
    "git commit all": "{f1}git commit all",
    "git stage [changes]": "{f1}git stage changes {enter}",
    "git stage all [changes]": "{f1}git stage all changes {enter}",
    "git unstage [changes]": "{f1}git unstage {enter}",
    "git unstage all [changes]": "{f1}git unstage all changes {enter}",
    "git create branch": "{f1}git create branch",
    "git custom create branch ": "{f1}git create branch from",
    "git open changes ": "{f1}git open changes",
    "git discard changes ": "{f1}git discard changes",
}

non_repeat_mapping = {
    "take content": "{home}{s-end}",
    "copy content": "{home}{s-end}{c-c}{escape}",
    "cut content": "{home}{s-end}{c-v}",
    "delete content": "{home}{s-end}{backspace}",
    "file explorer": "{cs-e}",
    "source control": "{cs-g}g",
    "command palette": "{f1}",
    # "rename": "{f2}",
    "go to definition": "{f12}",
    "comment": "{c-slash}",
    "block comment": "{as-a}",
    "fuzzy": "{c-p}",
    "save file": f"{{{CMD_OR_CTRL}-s}}",
    "open recent": "{c-r}",
    "(search file) | (file search)": "{c-f}",
    "(search project) | (project search)": "{cs-f}",
    "(replace [in] file) | (file replace)": "{c-h}",
    "(replace [in] project) | (project replace)": "{cs-h}",
    "call that": "(){left}",
    "tab new": "{c-n}",
    "below line <n>": between(
        Key("c-g"), Function(lambda **k: Text(str(k["n"])).execute()), Key("enter"), Key("c-enter")
    ),
    "go to line": "{c-g}",
    "split editor": "{c-backslash}",
    "close editor": "{c-f4}",
    "format document": "{sa-f}",
    **git_commands,
}

if utils.IS_MAC:
    non_repeat_mapping["file explorer"] = "{ws-e}"
    non_repeat_mapping["comment"] = "{w-slash}"
    non_repeat_mapping["fuzzy"] = "{w-p}"
    non_repeat_mapping["tab new"] = "{w-n}"
    non_repeat_mapping["(search file) | (file search)"] = "{w-f}"
    non_repeat_mapping["(search project) | (project search)"] = "{ws-f}"
    non_repeat_mapping["(replace [in] file) | (file replace)"] = "{wa-f}"
    non_repeat_mapping["(replace [in] project) | (project replace)"] = "{sw-h}"
    non_repeat_mapping["file explorer"] = "{ws-e}"
    non_repeat_mapping["source control"] = "{cs-g}"

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
    "tab close": "{c-w}",
    "grab": "{c-d}",
    "expand": "{as-right}",
    "shrink": "{as-left}",
    "previous editor": "{c-k}{c-left}",
    "next editor": "{c-k}{c-right}",
    "move editor right": "{c-k}{left}",
    "move editor left": "{c-k}{right}",
    "higher": "{pageup}",
    "lower": "{pagedown}",
}

if utils.IS_MAC:
    repeat_mapping["tab left"] = "{wa-left}"
    repeat_mapping["tab right"] = "{wa-right}"
    repeat_mapping["new line"] = "{w-enter}"
    repeat_mapping["new line above"] = "{ws-enter}"
    repeat_mapping["new cursor"] = "{aw-down}"
    repeat_mapping["new cursor above"] = "{aw-up}"
    repeat_mapping["indent"] = "{w-]}"
    repeat_mapping["out dent"] = "{w-[}"
    repeat_mapping["tab close"] = "{w-w}"
    repeat_mapping["grab"] = "{w-d}"


utils.load_commands(
    contexts.vscode,
    commands=non_repeat_mapping,
    extras=[
        Choice("clip", vscode_utils.clip),
        Choice("movements_multiple", vscode_utils.movements_multiple),
        Choice("select_actions_multiple", vscode_utils.select_actions_multiple),
        Choice("movements", vscode_utils.movements),
        Choice("select_actions_single", vscode_utils.select_actions_single),
    ],
)
utils.load_commands(contexts.vscode, repeat_commands=repeat_mapping)
