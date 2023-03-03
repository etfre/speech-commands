import time
from dragonfly import *
import srabuilder.actions
from srabuilder import rules

functions = {
    "all": "all",
    "any": "any",
    "eye d": "id",
    "float": "float",
    "input": "input",
    "int": "int",
    "length": "len",
    "list": "list",
    "min": "min",
    "max": "max",
    "slice": "slice",
    "string": "str",
    "super": "super",
}

values = {
    "list": "[]",
    "dictionary": "{}",
    "true": "True",
    "false": "False",
    "none": "None",
}

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
    "line": Key("home, s-end"),
    "word": Key("cs-w"),
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


non_repeat_mapping = {
    "banana hammock": Text("wtf"),
    "start debugging": Key("f5"),
    "<clip> <movements>": Function(clip_move),
    "<clip> <movements_multiple> [<n>]": Function(clip_move),
    "<clip> <select_actions_multiple> [<n>]": Function(do_select),
    "<clip> <select_actions_single>": Function(do_select),
    "explorer": Key("cs-e"),
    "source control": Key("cs-g") + Key("g"),
    "command palette": Key("f1"),
    "rename": Key("f2"),
    "go to definition": Key("f12"),
    "comment": Key("c-k") + Key("c-c"),
    "uncomment": Key("c-k") + Key("c-u"),
    "fuzzy": Key("c-cmma"),
    "save file": Key("c-s"),
    "search file": Key("c-f"),
    "search project": Key("cs-f"),
    "replace [in] file": Key("c-h"),
    "replace [in] project": Key("cs-h"),
    "surround parentheses": srabuilder.actions.surround("(", ")"),
    "surround blocks": srabuilder.actions.surround("[", "]"),
    "surround single": srabuilder.actions.surround("'", "'"),
    "surround double": srabuilder.actions.surround('"', '"'),
    "call that": srabuilder.actions.between(Text("()"), Key("left")),
    "tab new": Key("c-n"),
    "line <n>": srabuilder.actions.between(
        Key("c-g"), Function(lambda **k: Text(str(k["n"])).execute()), Key("enter")
    ),
}

repeat_mapping = {
    "flip north": Key("a-up"),
    "flip south": Key("a-down"),
    "duplicate north": Key("as-up"),
    "duplicate south": Key("as-down"),
    "cursor north": Key("ca-up"),
    "cursor south": Key("ca-down"),
    "tab left": Key("c-pageup"),
    "tab right": Key("c-pagedown"),
    "new line": Key("c-enter"),
    "new line above": Key("cs-enter"),
    "out dent": Key("c-["),
    "indent": Key("c-]"),
    "tab close": Key("c-w"),
    "grab": Key("c-d"),
}


def rule_builder():
    builder = rules.RuleBuilder()
    builder.basic.append(
        MappingRule(
            mapping=non_repeat_mapping,
            exported=False,
            name="visual_studio_non_repeat",
            extras=[
                rules.num,
                Choice("clip", clip),
                Choice("movements_multiple", movements_multiple),
                Choice("select_actions_multiple", select_actions_multiple),
                Choice("movements", movements),
                Choice("select_actions_single", select_actions_single),
            ],
            defaults={"n": 1},
        )
    )
    builder.repeat.append(
        MappingRule(mapping=repeat_mapping, exported=False, name="visual_studio_repeat")
    )
    return builder