import time
import utils
import contexts
from dragonfly import *
from breathe import Breathe
from srabuilder.actions import surround, between
from srabuilder import rules

tags = {
    'button': 'button',
    'div': 'div',
}

def full_tag(**kw):
    tag = kw['tags']
    tag_text = f'<{tag}></{tag}>'
    Text(tag_text).execute()
    Key(f'left:{len(tag) + 3}').execute()


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
    "tag <tags>": Function(full_tag),
    "opening <tags>": '<%(tags)s>',
    "closing <tags>": '</%(tags)s>',
    "self closing <tags>": '<%(tags)s />',
    "import react": "import React from 'react';",
    "class name": 'className=',
    "on click": 'onClick={{}}{left}',
}

repeat_mapping = {
}

extras = [
    Choice("tags", tags),
]
utils.load_commands(
    contexts.react,
    commands=non_repeat_mapping,
    extras=extras
)
# utils.load_commands(contexts.vscode, repeat_commands=repeat_mapping)