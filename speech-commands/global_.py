from dragonfly import *
from dragonfly.windows.clipboard import Clipboard

import os
import contexts
import windows
import utils
from srabuilder import rules

basic_mapping = {
    "language javascript": Function(lambda: contexts.set_language(contexts.JAVASCRIPT)),
    "language python": Function(lambda: contexts.set_language(contexts.PYTHON)),
    "language see plus plus": Function(lambda: contexts.set_language(contexts.CPP)),
    "language oh camel": Function(lambda: contexts.set_language(contexts.OCAML)),
    "(clear | reset) language": Function(lambda: contexts.set_language(None)),
    "launch wsl": Text("wsl.exe") + Key("enter"),
    "type clipboard": Function(utils.type_clipboard)
}

repeat = {
    "alt tab": '{alt:down}{tab}',
}

def rule_builder():
    builder = rules.RuleBuilder()
    builder.merge(windows.rule_builder())
    return builder

utils.load_commands(None, basic_mapping)
utils.load_commands(None, repeat_commands=repeat)
