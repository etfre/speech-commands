from dragonfly import *
import srabuilder.actions
from srabuilder import rules
import utils

CMD_OR_CTRL = "w" if utils.IS_MAC else "c"

sites = {
    "hacker news": "news.ycombinator.com",
    "google news": "news.google.com",
    "read it": "reddit.com",
    "new york times": "nytimes.com",
    "something awful": "forums.somethingawful.com",
}

non_repeat_mapping = {
    "refresh": Key("f5"),
    "go to <sites>": f"{{{CMD_OR_CTRL}-l}}%(sites)s{{enter}}",
    # Function(
    #     lambda **kw: srabuilder.actions.between(
    #         Key("c-l"), Text(kw["sites"]), Key("enter")
    #     ).execute()
    # ),
    "navigate": f"{{{CMD_OR_CTRL}-l}}",
    "new tab": Key(f"{CMD_OR_CTRL}-t"),
}

repeat_mapping = {
    "tab left": Key("c-pageup"),
    "tab right": Key("c-pagedown"),
    "close tab": Key("c-w"),
    "go back": Key("a-left"),
    "go forward": Key("a-right"),
}

utils.load_commands(
    commands=non_repeat_mapping,
    repeat_commands=repeat_mapping,
    extras=[Choice("sites", sites)],
)