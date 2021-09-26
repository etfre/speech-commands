from dragonfly import *
import srabuilder.actions
from srabuilder import rules

sites = {
    "hacker news": "news.ycombinator.com",
    "google news": "news.google.com",
    "read it": "reddit.com",
    "new york times": "nytimes.com",
    "something awful": "forums.somethingawful.com",
}

non_repeat_mapping = {
    "refresh": Key("f5"),
    "go to <sites>": Function(
        lambda **kw: srabuilder.actions.between(
            Key("c-l"), Text(kw["sites"]), Key("enter")
        ).execute()
    ),
    "navigate": Key("c-l"),
    "new tab": Key("c-t"),
}

repeat_mapping = {
    "tab left": Key("c-pageup"),
    "tab right": Key("c-pagedown"),
    "close tab": Key("c-w"),
    "go back": Key("a-left"),
    "go forward": Key("a-right"),
}


def rule_builder():
    builder = rules.RuleBuilder()
    extras = [Choice("sites", sites)]
    builder.basic.append(
        MappingRule(
            mapping=non_repeat_mapping,
            extras=extras,
            exported=False,
            name="chrome_non_repeat",
        )
    )
    builder.repeat.append(
        MappingRule(
            mapping=repeat_mapping, extras=extras, exported=False, name="chrome_repeat"
        )
    )
    return builder