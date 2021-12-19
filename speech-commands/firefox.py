from dragonfly import *
import srabuilder.actions
from srabuilder import rules
import utils
import contexts

sites = {
    "hacker news": "news.ycombinator.com",
    "google news": "news.google.com",
    "read it": "reddit.com",
    "new york times": "nytimes.com",
    "something awful": "forums.somethingawful.com",
}

values = {
    "list": "[]",
    "dictionary": "{}",
    "true": "True",
    "false": "False",
    "none": "None",
}

non_repeat_mapping = {
    "refresh": Key("f5"),
    "go to <sites>": Function(
        lambda **kw: srabuilder.actions.between(
            Key("c-l"), Text(kw["sites"]), Key("enter")
        ).execute()
    ),
    "navigate": Key("c-l"),
    "new tab": "{c-t}",
}

repeat_mapping = {
    "tab left": Key("c-pageup"),
    "tab right": Key("c-pagedown"),
    "close tab": Key("c-w"),
    "go back": Key("a-left"),
    "go forward": Key("a-right"),
}


extras = [Choice("sites", sites)]
utils.load_commands(context=contexts.firefox,
    repeat_commands=repeat_mapping, commands=non_repeat_mapping, extras=extras
)
