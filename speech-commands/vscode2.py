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
from typing import List, Dict, Any

RPC_INPUT_FILE = os.path.join(tempfile.gettempdir(), "speech-commands-input.json")
RPC_OUTPUT_FILE = os.path.join(tempfile.gettempdir(), "speech-commands-output.json")
RESPONSES_DICT: Dict[str, Any] = {}


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


def select_node(patternOrPatterns: str | List[str], direction: str, select_type: str, on_done: str):
    patterns = [patternOrPatterns] if isinstance(patternOrPatterns, str) else patternOrPatterns
    params = {
        "patterns": patterns,
        "type": patternOrPatterns,
        "direction": direction,
        "count": 1,
        "selectType": select_type,
        "onDone": on_done,
    }
    send_request("SELECT_NODE", params)


def format_request(method: str, params=None) -> dict:
    request_id = str(uuid.uuid4())
    request = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params:
        request["params"] = params
    return request


def send_request(method: str, params=None):
    request = format_request(method, params)
    request_id = request['id']
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


def move_until(char: str, count: int, include_pattern=False, reverse=False, move=False):
    char = re.escape(char)
    params = {
        "count": count,
        "pattern": char,
        "isPatternInclude": include_pattern,
        "reverse": reverse,
        "isMove": move,
    }
    resp = send_request("SELECT_UNTIL_PATTERN", params=params)
    print(resp)


def select_balanced(left: str, right: str, count: int, include_pattern=False, reverse=False, move=False):
    left = re.escape(left)
    right = re.escape(right)
    params = {
        "count": count,
        "left": left,
        "right": right,
        "isPatternInclude": include_pattern,
    }
    send_request("SELECT_IN_SURROUND", params=params)

def go_to_line(line: int):
    send_request("GO_TO_LINE", params={"line": line - 1})

def execute_command(command: str, *args):
    params = {"command": command, "args": args}
    send_request("EXECUTE_COMMAND", params=params)

cmds = {
    "[<digits>] take parentheses": df.Function(lambda **kw: select_balanced("(", ")", count=int(kw["digits"]))),
    "[<digits>] until <all_chars>": df.Function(lambda **kw: move_until(kw["all_chars"], int(kw["digits"]), move=True)),
    "[<digits>] take until <all_chars>": df.Function(lambda **kw: move_until(kw["all_chars"], int(kw["digits"]))),
    "[<digits>] after <all_chars>": df.Function(
        lambda **kw: move_until(kw["all_chars"], int(kw["digits"]), include_pattern=True, move=True)
    ),
    "[<digits>] take after <all_chars>": df.Function(
        lambda **kw: move_until(kw["all_chars"], int(kw["digits"]), include_pattern=True)
    ),
    "[<digits>] retreat <all_chars>": df.Function(
        lambda **kw: move_until(kw["all_chars"], int(kw["digits"]), reverse=True, move=True)
    ),
    "[<digits>] take retreat <all_chars>": df.Function(
        lambda **kw: move_until(kw["all_chars"], int(kw["digits"]), reverse=True)
    ),
    "[<digits>] before <all_chars>": df.Function(
        lambda **kw: move_until(
            kw["all_chars"],
            int(kw["digits"]),
            reverse=True,
            include_pattern=True,
            move=True,
        )
    ),
    "[<digits>] select before <all_chars>": df.Function(
        lambda **kw: move_until(kw["all_chars"], int(kw["digits"]), reverse=True, include_pattern=True)
    ),
    "go <n>": df.Function(lambda **k: go_to_line(k['n'])),

}

clip_corgi = {
    "take": "select",
    "copy": "copy",
    "cut": "cut",
    "kill": "delete",
}


utils.load_commands(
    contexts.vscode,
    commands=cmds,
    extras=[
        df.Choice("all_chars", {**keyboard.all_chars, **keyboard.digits}),
        df.Choice("digits", keyboard.digits),
    ],
    defaults={"digits": 1},
)

directions = {
    "previous": "before",
    "next": "after",
}


def select_with_index_or_slice(node, direction: str, index_or_slice: str, on_done: str):
    print(node, index_or_slice)
    pattern = node.format(index_or_slice)
    select_node(pattern, direction, "each", on_done)


def create_format_map(nodes: Dict[str, List[str] | str]) -> Dict[str, List[str] | str]:
    str_formatter = string.Formatter()
    format_map: Dict[str, List[str] | str] = {}
    for utterance, patternOrPatterns in nodes.items():
        is_str = isinstance(patternOrPatterns, str)
        patterns = [patternOrPatterns] if is_str else patternOrPatterns
        format_patterns = []
        for pattern in patterns:
            has_format_field = any((tup[1] == "0" for tup in str_formatter.parse(pattern)))
            pattern_with_format_field = pattern if has_format_field else pattern + "{0}"
            temp = pattern_with_format_field.replace("{0}", "temp-placeholder")
            temp = temp.replace("{", "{{").replace("}", "}}")
            pattern_with_format_field = temp.replace("temp-placeholder", "{0}")
            format_patterns.append(pattern_with_format_field)
        format_map[utterance] = format_patterns[0] if is_str else format_patterns
    return format_map


def remove_fields(nodes: Dict[str, List[str] | str]) -> None:
    removed_fields_map: Dict[str, List[str] | str] = {}
    for utterance, patternOrPatterns in nodes.items():
        is_str = isinstance(patternOrPatterns, str)
        patterns = [patternOrPatterns] if is_str else patternOrPatterns
        removed_fields_patterns = []
        for pattern in patterns:
            pattern_with_removed_format_field = pattern.replace("{0}", "")
            removed_fields_patterns.append(pattern_with_removed_format_field)
        removed_fields_map[utterance] = removed_fields_patterns[0] if is_str else removed_fields_patterns
    return removed_fields_map


def load_language_commands(context: df.Context, nodes: Dict[str, List[str] | str]):
    format_nodes = create_format_map(nodes)
    removed_fields_map = remove_fields(nodes)
    print(format_nodes)
    print(removed_fields_map)
    commands = {
        "<clip> <node>": df.Function(lambda **kw: select_node(kw["node"], "up", "block", kw["clip"])),
        "<clip> <direction> <node>": df.Function(
            lambda **kw: select_node(kw["node"], kw["direction"], "block", kw["clip"])
        ),
        "<clip> every <format_node>": df.Function(
            lambda **kw: select_with_index_or_slice(kw["format_node"], "up", "[]", kw["clip"])
        ),
        "<clip> every <direction> <format_node>": df.Function(
            lambda **kw: select_with_index_or_slice(kw["format_node"], kw["direction"], "[]", kw["clip"])
        ),
    }
    extras = [
        df.Choice("clip", clip_corgi),
        df.Choice("node", removed_fields_map),
        df.Choice("direction", directions),
        df.Choice("format_node", format_nodes),
    ]

    utils.load_commands(context, commands=commands, extras=extras)
