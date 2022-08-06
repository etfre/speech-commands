import time
import utils
import contexts
import keyboard
import dragonfly as df
from breathe import Breathe
from srabuilder.actions import surround, between
from srabuilder import rules

def invoke():
    df.Key('c-k').execute()
    df.Key('i').execute()

def move_until(char: str, count: int, include_pattern=False, reverse=False, move=False):
    char = '\\' + char
    invoke()
    time.sleep(0.1)
    text = char
    extensions = 'i'
    if count > 1:
        extensions += str(count)
    if move:
        extensions += "m"
    if reverse:
        extensions += 'r'
    if include_pattern:
        extensions += 'c'
    if extensions:
        text += '/' + extensions
    df.Text(text).execute()
    df.Key('enter').execute()

cmds = {
    "[<digits>] until <all_chars>": df.Function(lambda **kw: move_until(kw['all_chars'], int(kw['digits']), move=True)),
    "[<digits>] select until <all_chars>": df.Function(lambda **kw: move_until(kw['all_chars'], int(kw['digits']))),
    "[<digits>] after <all_chars>": df.Function(lambda **kw: move_until(kw['all_chars'], int(kw['digits']), include_pattern=True, move=True)),
    "[<digits>] select after <all_chars>": df.Function(lambda **kw: move_until(kw['all_chars'], int(kw['digits']), include_pattern=True)),
    "[<digits>] retreat <all_chars>": df.Function(lambda **kw: move_until(kw['all_chars'], int(kw['digits']), reverse=True, move=True)),
    "[<digits>] select retreat <all_chars>": df.Function(lambda **kw: move_until(kw['all_chars'], int(kw['digits']), reverse=True)),
    "[<digits>] before <all_chars>": df.Function(lambda **kw: move_until(kw['all_chars'], int(kw['digits']), reverse=True, include_pattern=True, move=True)),
    "[<digits>] select before <all_chars>": df.Function(lambda **kw: move_until(kw['all_chars'], int(kw['digits']), reverse=True, include_pattern=True)),
}
# * +
utils.load_commands(
    contexts.vscode,
    commands=cmds,
    extras=[
        df.Choice("all_chars", {**keyboard.all_chars, **keyboard.digits}),
        df.Choice('digits', keyboard.digits),
    ],  
    defaults={'digits': 1}
)