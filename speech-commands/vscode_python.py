from dragonfly import *
import utils
import re
import contexts
import vscode2
from typing import List, Dict

node_map = {
    "block": "block",
    "class body": "decorated_definition?.class_definition.block",
    "class deaf": "decorated_definition?.class_definition",
    "class name": "decorated_definition?.class_definition.*[1]",
    "comparison": "comparison_operator",
    "func body": "decorated_definition?.function_definition.block",
    "func deaf": "decorated_definition?.function_definition",
    # "constructor": "decorated_definition?.function_definition.*@name(__init__)",
    "func name": "decorated_definition?.function_definition.*[1]",
    "list": "list",
    "list comprehension": "list_comprehension",
    "dictionary comprehension": "dictionary_comprehension",
    "if state": "if_statement",
    "item": "(list | tuple).*@isNamed",
    "while state": "while_statement",
    "for state": "for_statement",
    "try state": "try_statement",
    "try clause": "try_statement.*[0:3]",
    "except clause": "except_clause",
    "finally clause": "finally_clause",
    "with state": "with_statement",
    "if clause": "if_statement.*[:4]", 
    "if condition": "if_statement.*[1]",
    "else if clause": "elif_clause",
    "else if body": "elif_clause.block",
    "else clause": "else_clause",
    "pair": "dictionary.pair",
    "else body": "else_clause.block",
    "dictionary": "dictionary",
    "string": "string",
    "two pull": "tuple",
    "assignment": "assignment",
    "left": "assignment.*[0]",
    "right": "assignment.*[2]",
    "arguments": "argument_list",
    "pass": "pass",
    "key": "pair{0}.*[0]",
    "value": "pair{0}.*[2]",
    "parameters": "parameters",
    "param": "function_definition.parameters.*@isNamed",
    # "constructor": "decorated_definition?.class_definition.block.function_definition.*@name(__init__)",
    "constructor": "decorated_definition?.class_definition.block.function_definition@mark.*@name(__init__)",
    # "param": "function_definition.parameters.*@named",
    "arguments": "argument_list",
    "arg": "argument_list.*@isNamed",
    "call": "call",
    "attribute": "attribute",
    "ident": "identifier",
    "assignment": "assignment",
    "expression": "expression",
    "statement": "(_simple_statement | _compound_statement)",
    # "statement": "*@oneOf(_simple_statement, _compound_statement)",
    "block": "block",
    # "statement": "_simple_statement",
}

vscode2.load_language_commands(contexts.python & contexts.vscode, node_map)
