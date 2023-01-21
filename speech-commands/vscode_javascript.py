from dragonfly import *
import utils
import re
import contexts
import vscode_utils
import vscode2
from typing import List, Dict

node_map = {
    "block": "block",
    "expression": "expression",
    # "param": "formal_parameters.*",
    "param": "formal_parameters.*{1:-1:2}",
}

vscode2.load_language_commands(contexts.javascript & contexts.vscode, node_map)
