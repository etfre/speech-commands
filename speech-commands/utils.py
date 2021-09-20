import dragonfly as df
import srabuilder
import srabuilder.actions
from srabuilder import rules


digitMap = {
    "zero": 0,
    "one": 1,
    "too": 2,
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
    "too": 2,
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


positive_digits = df.Sequence(
    [df.Choice(None, nonZeroDigitMap), df.Repetition(df.Choice(None, digitMap), min=0, max=2)],
    name="positive_digits",
)
positive_num = df.Alternative([df.Modifier(positive_digits, parse_numrep), df.Choice(None, ten_through_twelve)], name="n")
positive_index = df.RuleWrap("positive_index", df.Modifier(positive_num, lambda x: x - 1))
positive_index2 = df.RuleWrap("positive_index2", df.Modifier(positive_num, lambda x: x - 1))

def load_commands(context=None, commands=None, repeat_commands=None, extras=(), defaults=None, ccr=True):
    from breathe import Breathe 
    if defaults is None:
        defaults = {}
    defaults.update({'n': 1, 'positive_index': 0})
    if extras is None:
        extras = ()
    extras = tuple(extras) + (positive_num, positive_index)
    if commands:
        commands = {k: srabuilder.actions.parse(v) if isinstance(v, str) else v for k, v in commands.items()}
        Breathe.add_commands(context, commands, ccr=ccr, defaults=defaults, extras=extras)
    if repeat_commands:
        formatted_repeat_commands = {}
        for rule, action in repeat_commands.items():
            rule = f'[<n>] {rule}'
            action = srabuilder.actions.parse(action) if isinstance(action, str) else action
            formatted_repeat_commands[rule] = action * df.Repeat(extra='n')
        Breathe.add_commands(context, formatted_repeat_commands, ccr=ccr, defaults=defaults, extras=extras)

def read_env_file(path: str) -> dict:
    variables = {}
    with open(path) as f:
        for line in f:
            if not line.startswith('#'):
                key, val = line.replace('\n', '').split('=')
                variables[key] = val
    return variables

try:
    env = read_env_file('..\\.env')
except FileNotFoundError:
    env = {}
print(env)