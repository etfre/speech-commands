from dragonfly import *
import utils
import re
import contexts
import vscode_utils
import vscode2
from typing import List, Dict

node_map = {
    "function definition": "decorated_definition?.function_definition",
    "(item | pair)": "dictionary.pair",
    "block": "block",
    "list": "list",
    "if statement": "if_statement",
    "if clause": "if_statement.*[:4]", 
    "if condition": "if_statement.*[1]",
    "else if [clause | clauses]": "if_statement.elif_clause",
    "else [clause | clauses]": "if_statement.else_clause",
    "dictionary": "dictionary",
    "string": "string",
    "assignment": "assignment",
    "arguments": "argument_list",
    "pass": "pass",
    "key": "pair{0}.*[0]",
    "value": "pair{0}.*[2]",
    "param list": "parameters.*[1:-1]",
    "param": "function_definition.parameters.*{1:-1:2}",
    "call": "call",
    "attribute": "attribute",
    "name": "identifier",
}

vscode2.load_language_commands(contexts.python & contexts.vscode, node_map)
