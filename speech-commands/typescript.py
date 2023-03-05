from dragonfly import *
import srabuilder.actions
from srabuilder import rules

import utils, vscode2
import contexts


functions = {
}

namespaces = {
}

mapping = {
    "interface": "interface ",
    "type": vscode2.insert_padded("type "),
    "key of": vscode2.insert_padded("keyof "),
    "annotate": vscode2.insert_padded(": "),
    "implements": vscode2.insert_padded("implements "),
    "extends": vscode2.insert_padded("extends "),
    "generic": "<>{left}",
}

extras = [Choice("functions", functions), Choice("namespaces", namespaces)]
utils.load_commands(contexts.typescript, commands=mapping, extras=extras)
