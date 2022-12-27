from dragonfly import *
import utils
import re
import contexts
import vscode_utils
import vscode2
from typing import List, Dict

node_map = {
    "block": "block",
}

vscode2.load_language_commands(contexts.ocaml & contexts.vscode, node_map)
