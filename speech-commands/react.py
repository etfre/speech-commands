import time
import utils
import contexts
from dragonfly import *
from breathe import Breathe
from srabuilder.actions import surround, between
from srabuilder import rules

tags = {
    "body": "body",
    "button": "button",
    "canvas": "canvas",
    "div": "div",
    "empty": "",
    "heading one": "h1",
    "heading too": "h2",
    "heading three": "h3",
    "heading four": "h4",
    "heading five": "h5",
    "heading six": "h6",
    "hyperlink": "a",
    "image": "img",
    "input": "input",
    "label": "label",
    "line break": "br",
    "list item": "li",
    "ordered list": "ol",
    "paragraph": "p",
    "span": "span",
    "table": "table",
    "unordered list": "ul",
}

attributes = {}


def full_tag(**kw):
    tag = kw["tags"]
    tag_text = f"<{tag}></{tag}>"
    Text(tag_text).execute()
    Key(f"left:{len(tag) + 3}").execute()

non_repeat_mapping = {
    "tag <tags>": Function(full_tag),
    "opening <tags>": "<%(tags)s>",
    "closing <tags>": "</%(tags)s>",
    "self closing <tags>": "<%(tags)s />",
    "import react": "import React from 'react';",
    "class name": "className=",
    "on click": "onClick={{}}{left}",
    "use effect": "useEffect(() => {{}});{left:3}{enter}",
    "react": "React",
    "new (function | functional) component": utils.snippet("functional-component.tsx")
    + Key("c-f")
    + Text("App")
    + Key("c-d:2")
    + Key("escape"),
}

repeat_mapping = {}

extras = [
    Choice("tags", tags),
]
utils.load_commands(contexts.react, commands=non_repeat_mapping, extras=extras)
# utils.load_commands(contexts.vscode, repeat_commands=repeat_mapping)
