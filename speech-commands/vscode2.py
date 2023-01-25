import time
import string
import tempfile
import threading
import re
import os
import os.path
import keyboard
import uuid
import json
import contexts
import queue
import dragonfly as df
import utils
import vscode_utils
from breathe import Breathe
from srabuilder.actions import surround, between
from srabuilder import rules
from typing import Any

RPC_INPUT_FILE = os.path.join(tempfile.gettempdir(), "speech-commands-input.json")
RPC_OUTPUT_FILE = os.path.join(tempfile.gettempdir(), "speech-commands-output.json")
RESPONSES_DICT: dict[str, Any] = {}


def watch_output_file():
    prev_stamp = 0
    while True:
        stamp = os.stat(RPC_OUTPUT_FILE).st_mtime
        if stamp != prev_stamp:
            with open(RPC_OUTPUT_FILE) as f:
                text = f.read()
                try:
                    resp = json.loads(text)
                except json.decoder.JSONDecodeError:
                    pass
                else:
                    RESPONSES_DICT[resp["id"]] = (resp, stamp)
            prev_stamp = stamp
        time.sleep(0.01)


threading.Thread(target=watch_output_file, daemon=True).start()


def commands_per_selecion(**kw):
    action = kw.get("select_action", "move")
    on_done = create_on_done(action)
    move_commands, select_commands = kw['command_select_target']
    params = {
        "count": kw.get('digits', 1),
        "commands": move_commands if action == "move" else select_commands,
        "onDone": on_done
    }
    return send_request("EXECUTE_COMMANDS_PER_SELECTION", params)

def smart_action_text(**kw):
    direction = "backwards" if "back" in kw["_node"].words() else "forwards"
    side = kw.get("side", "start" if direction == "backwards" else "end")
    pattern = re.escape(kw["all_chars"])
    params = {
        "target": {"pattern": pattern, "count": kw.get("digits", 1), "side": side},
        "direction": direction,
    }
    action = kw.get("select_action", "move")
    params["onDone"] = None if action in ("move", "select", "extend") else action
    if action != "move":
        action = "extend"
    return smart_action_request(action, params)


def create_on_done(action: str):
    if action == "cut":
        return {"type": "executeCommand", "commandName": "editor.action.clipboardCutAction"}
    if action == "copy":
        return {"type": "executeCommand", "commandName": "editor.action.clipboardCopyAction"}
    if action == "paste":
        return {"type": "executeCommand", "commandName": "editor.action.clipboardPasteAction"}
    if action == "rename":
        return {"type": "executeCommand", "commandName": "editor.action.rename"}


def smart_action_node(**kw):
    get_every = "every" in kw["_node"].words()
    node = kw["node"]
    params = {"target": {"selector": node, "getEvery": get_every}, "direction": kw.get("direction", "smart")}
    action = kw["action"]
    if action in ("start", "end"):
        params["target"]["side"] = action
        action = "move"
    if action == "extend" and params["direction"] == "smart":
        params["direction"] = "forwards"
    params["onDone"] = create_on_done(action)
    if params["onDone"]:
        action = "select"
    return smart_action_request(action, params)


def smart_action_request(action: str, params: dict):
    assert "action" not in params
    return send_request("SMART_ACTION", {**params, "action": action})


def format_request(method: str, params=None) -> dict:
    request_id = str(uuid.uuid4())
    request = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params:
        request["params"] = params
    return request


def send_request(method: str, params=None):
    request = format_request(method, params)
    request_id = request["id"]
    with open(RPC_INPUT_FILE, "w") as f:
        json.dump(request, f)
    return get_response(request_id)


def get_response(request_id: str):
    val = RESPONSES_DICT.get(request_id)
    start_time = time.time()
    while True:
        curr_time = time.time()
        val = RESPONSES_DICT.get(request_id)
        if val is not None:
            break
        if curr_time - start_time > 5:
            raise TimeoutError
        time.sleep(0.01)
    try:
        del RESPONSES_DICT[request_id]
    except KeyError:
        pass
    resp, _ = val
    return resp


def select_balanced(
    action: str, left: str | None, right: str | None, count: int = 1, include_last_match=True, on_done=None
):
    params = {
        "action": action,
        "count": count,
        "left": left,
        "right": right,
        "onDone": on_done,
        "includeLastMatch": include_last_match,
    }
    send_request("SELECT_IN_SURROUND", params=params)


def surround_replace(**kw):
    action = "select"
    count = kw.get("digits", 1)
    surround = kw.get("surround", (None, None))
    left = utils.re_escape_or_none(surround[0])
    right = utils.re_escape_or_none(surround[1])
    on_done = {
        "type": "surroundReplace",
        "left": kw["surround_literal"][0],
        "right": kw["surround_literal"][1],
    }
    select_balanced(action, left, right, count=count, on_done=on_done)


def surround_insert(**kw):
    left, right = kw["surround_literal"]
    params = {
        "left": left,
        "right": right,
    }
    send_request("SURROUND_INSERT", params=params)


def go_to_line(line: int):
    send_request("GO_TO_LINE", params={"line": line - 1})


def execute_command(command: str, *args):
    params = {"command": command, "args": args}
    send_request("EXECUTE_COMMAND", params=params)


def execute_commands_each_selection(commands: list, *args):
    params = {"commands": commands, "args": args}
    send_request("EXECUTE_COMMANDS_EACH_SELECTION", params=params)


other_target_ranges = {
    "word": (r"[a-z0-9_]+", r"[a-z0-9_]", r"[^a-z0-9_]"),
    "content": (r"(?<=^\s*).+$", r"(?<=^\s*).", r"$"),
}

command_select_targets = {
    "first": (["cursorHome"], ["cursorHomeSelect"]),
    "final": (["cursorEnd"], ["cursorEndSelect"]),
    "north": (["cursorUp"], ["cursorUpSelect"]),
    "east": (["cursorRight"], ["cursorRightSelect"]),
    "south": (["cursorDown"], ["cursorDownSelect"]),
    "west": (["cursorLeft"], ["cursorLeftSelect"]),
    # "content": (["cursorEnd"], ["cursorEndSelect"]),
}

sides = {
    "pre": "start",
    "post": "end",
}

select_actions = {
    "take": "select",
    "copy": "copy",
    "cut": "cut",
    "change": "delete",
    "extend": "extend",
    "rename": "rename",
}

actions = {**sides, **select_actions}

directions = {
    "previous": "backwards",
    "next": "forwards",
}


def smart_action_node_with_index_or_slice(kw, index_or_slice: str):
    kw["node"] = kw["format_node"].format(index_or_slice)
    del kw["format_node"]
    return smart_action_node(**kw)


def create_format_map(nodes: dict[str, str]) -> dict[str, str]:
    str_formatter = string.Formatter()
    format_map: dict[str, str] = {}
    for utterance, pattern in nodes.items():
        has_format_field = any((tup[1] == "0" for tup in str_formatter.parse(pattern)))
        pattern_with_format_field = pattern if has_format_field else pattern + "{0}"
        temp = pattern_with_format_field.replace("{0}", "temp-placeholder")
        temp = temp.replace("{", "{{").replace("}", "}}")
        pattern_with_format_field = temp.replace("temp-placeholder", "{0}")
        format_map[utterance] = pattern_with_format_field
    return format_map


def remove_fields(nodes: dict[str, str]) -> None:
    removed_fields_map: dict[str, str] = {}
    for utterance, pattern in nodes.items():
        pattern_with_removed_format_field = pattern.replace("{0}", "")
        removed_fields_map[utterance] = pattern_with_removed_format_field
    return removed_fields_map


def load_language_commands(context: df.Context, nodes: dict[str, str]):
    format_nodes = create_format_map(nodes)
    removed_fields_map = remove_fields(nodes)
    commands = {
        "<action> [<direction>] <node>": smart_action_node,
        "<action> every [<direction>] <format_node>": df.Function(
            lambda **kw: smart_action_node_with_index_or_slice(kw, "[]")
        ),
    }
    extras = [
        df.Choice("action", actions),
        df.Choice("node", removed_fields_map),
        df.Choice("direction", directions),
        df.Choice("format_node", format_nodes),
    ]

    utils.load_commands(context, commands=commands, extras=extras)


surround_literals = {
    "parentheses": ("(", ")"),
    "braces": ("{", "}"),
    "brackets": ("[", "]"),
    "doubles": ('"', '"'),
    "singles": ("'", "'"),
    "backquotes": ("`", "`"),
    "(triples | (three | triple) doubles)": ('"""', '"""'),
}

surround = {"bounds": (None, None), **surround_literals}

cmds = {
    "[<digits>] <action> [inside] <surround>": df.Function(
        lambda **kw: select_balanced(
            kw["action"],
            None if  kw["surround"][0] is None else re.escape(kw["surround"][0]),
            None if kw["surround"][1] is None else re.escape(kw["surround"][1]),
            count=int(kw["digits"]),
            include_last_match="inside" not in kw["_node"].words(),
        )
    ),
    "[<digits>] swap [<surround>] [for | with] <surround_literal>": df.Function(surround_replace),
    "surround <surround_literal>": df.Function(surround_insert),
    "[<digits>] [back] ((<select_action> [<side>]) | <side>) <all_chars>": df.Function(smart_action_text),
    "[<digits>] [<select_action>] <command_select_target>": df.Function(commands_per_selecion),
    "go <n>": df.Function(lambda **k: go_to_line(k["n"])),
}

all_chars_rep = df.Repetition(
    df.Choice(None, {**keyboard.all_chars, **{k: str(v) for k, v in keyboard.digits.items()}}),
    name="all_chars",
    min=1,
    max=16,
)
all_chars = df.Modifier(all_chars_rep, lambda l: "".join(l))

utils.load_commands(
    contexts.vscode,
    commands=cmds,
    extras=[
        all_chars,
        df.Choice("digits", keyboard.digits),
        df.Choice("side", sides),
        df.Choice("select_action", select_actions),
        df.Choice("action", actions),
        df.Choice("direction", directions),
        df.Choice("surround_literal", surround_literals),
        df.Choice("surround", surround),
        df.Choice("other_target_range", other_target_ranges),
        df.Choice("command_select_target", command_select_targets),
    ],
    defaults={"digits": 1},
)
