from dragonfly import *

import contexts
import keyboard
import mouse
import windows
from srabuilder import rules


basic_mapping = {
    "language javascript": Function(lambda: contexts.set_language(contexts.JAVASCRIPT)),
    "language python": Function(lambda: contexts.set_language(contexts.PYTHON)),
    "launch wsl": Text("wsl.exe") + Key("enter"),
}


def rule_builder():
    builder = rules.RuleBuilder()
    builder.repeat.append(keyboard.root_rule())
    builder.repeat.append(mouse.root_rule())
    builder.basic.append(
        MappingRule(mapping=basic_mapping, exported=False, name="state_basic")
    )
    builder.merge(windows.rule_builder())
    return builder