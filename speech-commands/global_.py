from dragonfly import *

import contexts
import mouse
import windows
import utils
from srabuilder import rules


basic_mapping = {
    "language javascript": Function(lambda: contexts.set_language(contexts.JAVASCRIPT)),
    "language python": Function(lambda: contexts.set_language(contexts.PYTHON)),
    "(clear | reset) language": Function(lambda: contexts.set_language(None)),
    "launch wsl": Text("wsl.exe") + Key("enter"),
}

repeat = {
    "alt tab": '{alt:down}{tab}',
}

def rule_builder():
    builder = rules.RuleBuilder()
    # builder.repeat.append(keyboard.root_rule())
    builder.repeat.append(mouse.root_rule())
    # builder.basic.append(
    #     MappingRule(mapping=basic_mapping, exported=False, name="state_basic")
    # )
    builder.merge(windows.rule_builder())
    return builder

utils.load_commands(None, basic_mapping)
utils.load_commands(None, repeat_commands=repeat)
