import dragonfly as df
import re
from functools import wraps
import errno
import os
import signal
import time
import os.path
import srabuilder
import srabuilder.actions
from srabuilder import rules
import platform
from typing import Dict, Iterator

IS_MAC = platform.system() == "Darwin"
CMD_OR_CTRL = "w" if IS_MAC else "c"

digitMap = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

nonZeroDigitMap = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

ten_through_twelve = {
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
}


def parse_numrep(rep):
    first, rest = rep
    numstr = str(first) + "".join(str(d) for d in rest)
    return int(numstr)


def parse_numrep2(rep):
    return int("".join(str(d) for d in rep))


positive_digits = df.Sequence(
    [
        df.Choice(None, nonZeroDigitMap),
        df.Repetition(df.Choice(None, digitMap), min=0, max=2),
    ],
    name="positive_digits",
)
positive_digit = df.Choice("positive_digit", nonZeroDigitMap)
positive_num = df.Alternative(
    [df.Modifier(positive_digits, parse_numrep), df.Choice(None, ten_through_twelve)],
    name="n",
)
positive_index = df.RuleWrap("positive_index", df.Modifier(positive_num, lambda x: x - 1))
positive_index2 = df.RuleWrap("positive_index2", df.Modifier(positive_num, lambda x: x - 1))
numrep = df.RuleWrap("num", df.Repetition(df.Choice(None, digitMap), min=0, max=10))
num = df.Modifier(numrep, parse_numrep2)

def _make_num_rule(first_digit_choice: dict[str, int], remaining_digits_count: int, name: str):
    if remaining_digits_count == 0:
        choices = df.Choice(None, first_digit_choice)
    else:
        choice = df.Choice(None, digitMap) 
        second_item = choice if remaining_digits_count == 1 else df.Repetition(choice, min=0, max=remaining_digits_count)
        choices = df.Sequence([
            df.Choice(None, first_digit_choice),
            second_item,
        ])
    return df.RuleWrap(name, df.Modifier(choices, parse_numrep))
                       
def make_num_rule(name: str, remaining_digits_count):
    return _make_num_rule(nonZeroDigitMap, remaining_digits_count, name)
                       

def load_commands(
    context: df.Context | None = None,
    commands: Dict[str, df.ActionBase | str] | None = None,
    repeat_commands: Dict[str, df.ActionBase | str] | None = None,
    extras: Iterator[df.ElementBase] = (),
    defaults=None,
    ccr=True,
):
    from breathe import Breathe

    if defaults is None:
        defaults = {}
    defaults = {**defaults, **{"n": 1, "positive_index": 0, "positive_digit": 1}}
    if extras is None:
        extras = ()
    extras = tuple(extras) + (positive_num, positive_index)
    if commands:
        commands = {k: srabuilder.actions.parse(v) if isinstance(v, str) else v for k, v in commands.items()}
        Breathe.add_commands(context, commands, ccr=ccr, defaults=defaults, extras=extras)
    if repeat_commands:
        formatted_repeat_commands = {}
        for rule, action in repeat_commands.items():
            rule = f"[<n>] {rule}"
            action = srabuilder.actions.parse(action) if isinstance(action, str) else action
            formatted_repeat_commands[rule] = action * df.Repeat(extra="n")
        Breathe.add_commands(
            context,
            formatted_repeat_commands,
            ccr=ccr,
            defaults=defaults,
            extras=extras,
        )


def read_env_file(path: str) -> dict:
    variables = {}
    with open(path) as f:
        for line in f:
            if not line.startswith("#"):
                try:
                    key, val = line.replace("\n", "").split("=")
                except ValueError:
                    pass
                else:
                    variables[key] = val
    return variables


try:
    env = read_env_file(os.path.join("..", ".env"))
except FileNotFoundError:
    env = {}


def type_text(lines):
    for i, line in enumerate(lines):
        if line:
            df.Text(line).execute()
        if i != len(lines) - 1:
            df.Key("escape").execute()
            df.Key("enter").execute()
            df.Key("home").execute()


def type_clipboard():
    instance = df.Clipboard()  # Create empty instance.
    instance.copy_from_system()  # Retrieve from system clipboard.
    if not instance.text:
        return
    lines = instance.text.split(os.linesep)
    type_text(lines)


def snippet(fname: str):
    def inner():
        with open(os.path.join("snippets", fname)) as f:
            type_text([x.replace("\n", "").replace("\r", "") for x in f])

    return df.Function(inner)



class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL,seconds) #used timer instead of alarm
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator

def re_escape_or_none(val: str | None) -> str | None:
    return None if val is None else re.escape(val)