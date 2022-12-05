import time
import tempfile
import threading
import re
import os
import os.path
import keyboard
import utils
import uuid
import json
import contexts
import queue
import dragonfly as df
from breathe import Breathe
from srabuilder.actions import surround, between
from srabuilder import rules
from typing import List

RPC_INPUT_FILE = os.path.join(tempfile.gettempdir(), "speech-commands-input.json")
RPC_OUTPUT_FILE = os.path.join(tempfile.gettempdir(), "speech-commands-output.json")
RPC_RESPONSES = queue.Queue(maxsize=1)


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
                    while True:
                        try:
                            RPC_RESPONSES.get_nowait()
                        except queue.Empty:
                            break
                    RPC_RESPONSES.put_nowait(resp)
            prev_stamp = stamp
        time.sleep(0.1)


threading.Thread(target=watch_output_file, daemon=True).start()

def select_node(patternOrPatterns: str | List[str], direction: str):
    patterns = [patternOrPatterns] if isinstance(patternOrPatterns, str) else patternOrPatterns
    params = {"patterns": patterns, "type": patternOrPatterns, "direction": direction, "count": 1}
    send_request("SELECT_NODE", params)

def format_request(method: str, params=None) -> dict:
    request_id = str(uuid.uuid4())
    request = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params:
        request["params"] = params
    return request

def send_request(method: str, params=None, wait_for_response=False):
    request = format_request(method, params)
    with open(RPC_INPUT_FILE, "w") as f:
        json.dump(request, f)
    if wait_for_response:
        resp = RPC_RESPONSES.get(block=True, timeout=3)
        return resp

def send_requests(requests, wait_for_response=False):
    with open(RPC_INPUT_FILE, "w") as f:
        json.dump(requests, f)
    if wait_for_response:
        responses = RPC_RESPONSES.get(block=True, timeout=3)
        return responses


def move_until(char: str, count: int, include_pattern=False, reverse=False, move=False):
    char = re.escape(char)
    params = {
        "count": count,
        "pattern": char,
        "isPatternInclude": include_pattern,
        "reverse": reverse,
        "isMove": move,
    }
    send_request("SELECT_UNTIL_PATTERN", params=params)


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


cmds = {
    "[<digits>] select parentheses": df.Function(lambda **kw: select_balanced("(", ")", count=int(kw["digits"]))),
    "[<digits>] until <all_chars>": df.Function(lambda **kw: move_until(kw["all_chars"], int(kw["digits"]), move=True)),
    "[<digits>] select until <all_chars>": df.Function(lambda **kw: move_until(kw["all_chars"], int(kw["digits"]))),
    "[<digits>] after <all_chars>": df.Function(
        lambda **kw: move_until(kw["all_chars"], int(kw["digits"]), include_pattern=True, move=True)
    ),
    "[<digits>] select after <all_chars>": df.Function(
        lambda **kw: move_until(kw["all_chars"], int(kw["digits"]), include_pattern=True)
    ),
    "[<digits>] retreat <all_chars>": df.Function(
        lambda **kw: move_until(kw["all_chars"], int(kw["digits"]), reverse=True, move=True)
    ),
    "[<digits>] select retreat <all_chars>": df.Function(
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
}
# * +
utils.load_commands(
    contexts.vscode,
    commands=cmds,
    extras=[
        df.Choice("all_chars", {**keyboard.all_chars, **keyboard.digits}),
        df.Choice("digits", keyboard.digits),
    ],
    defaults={"digits": 1},
)
