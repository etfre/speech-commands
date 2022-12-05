from dragonfly import *
import utils
import re
import contexts
import vscode_utils
import vscode2

node_map = {
    "function definition": ["decorated_definition", "function_definition"],
    "every (item | pair)": "dictionary.pair[]",
    "block": "block",
    "list": "list",
    "if statement": "if_statement",
    "if clause": "if_statement.*[:4]", 
    "if condition": "if_statement.*[1]",
    "else if [clause | clauses]": "if_statement.elif_clause",
    "else [clause | clauses]": "if_statement.else_clause",
    "arguments": "argument_list"
}

snippets = {
    "function": (("def ", "async def ", "lambda "), re.compile("[^:]$")),
    "method": (("def ", "async def "), re.compile("[^:]$")),
    "class": ("class ", re.compile("[^:]$")),
    "list": ("[", re.compile("[\\]]$")),
    "dictionary": ("{", re.compile("[\\}]$")),
    "call": (re.compile(r'.*\('), re.compile("[\\)],*$")),
}

commands = {
    "select <node>": Function(lambda **kw: vscode2.select_node(kw['node'], "up")),
    "select previous <node>": Function(lambda **kw: vscode2.select_node(kw['node'], "before")),
    "select next <node>": Function(lambda **kw: vscode2.select_node(kw['node'], "after")),
}

extras = [
    Choice("clip", vscode_utils.clip),
    Choice("node", node_map),
    Choice("snippets", snippets),
]
utils.load_commands(contexts.python & contexts.vscode, commands=commands, extras=extras)
