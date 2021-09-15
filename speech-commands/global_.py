from dragonfly import *
from dragonfly.windows.clipboard import Clipboard

import os
import contexts
import windows
import utils
from srabuilder import rules


def type_clipboard():
    instance = Clipboard()        # Create empty instance.
    print(instance)
    instance.copy_from_system()   # Retrieve from system clipboard.
    if not instance.text:
        return
    lines = instance.text.split(os.linesep)
    for i, line in enumerate(lines):
        if line:
            Text(line).execute()
        if i != len(lines) - 1:
            Key('enter').execute()
            Key('home').execute()

basic_mapping = {
    "language javascript": Function(lambda: contexts.set_language(contexts.JAVASCRIPT)),
    "language python": Function(lambda: contexts.set_language(contexts.PYTHON)),
    "(clear | reset) language": Function(lambda: contexts.set_language(None)),
    "launch wsl": Text("wsl.exe") + Key("enter"),
    "type clipboard": Function(type_clipboard)
}

repeat = {
    "alt tab": '{alt:down}{tab}',
}

def rule_builder():
    builder = rules.RuleBuilder()
    # builder.repeat.append(keyboard.root_rule())
    # builder.repeat.append(mouse.root_rule())
    # builder.basic.append(
    #     MappingRule(mapping=basic_mapping, exported=False, name="state_basic")
    # )
    builder.merge(windows.rule_builder())
    return builder

utils.load_commands(None, basic_mapping)
utils.load_commands(None, repeat_commands=repeat)
