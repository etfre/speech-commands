from dragonfly import *
from srabuilder import rules

import urllib.parse
import time
import uuid
import os
import tempfile


def enter_command(cmd):
    Text(cmd).execute()
    Key("enter").execute()


basic = {
    "python": Text("python3 "),
    "pip": Text("pip "),
    "pip install": Text("pip install "),
    "pip freeze": Text("pip freeze > requirements.txt") + Key("enter"),
    "activate virtual": Text("source bin/activate") + Key("enter"),
    "create virtual": Text("python3 -m venv .") + Key("enter"),
    "flask run": Text("python -m flask run") + Key("enter"),
}


def rule_builder():
    builder = rules.RuleBuilder()
    extras = []
    defaults = {"n": 1}
    builder.basic.append(
        MappingRule(
            mapping=basic,
            extras=extras,
            exported=False,
            defaults=defaults,
            name="python_terminal_basic",
        )
    )
    return builder
