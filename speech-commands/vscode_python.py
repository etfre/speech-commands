from dragonfly import *
import utils
import re
import contexts
import vscode_utils
import vscode2

node_map = {
    "function definition": "function_definition"
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
    "<clip> <snippets>": Function(
        lambda **kw: vscode_utils.expand_while(
            first_check=kw["snippets"][0],
            last_check=kw["snippets"][1],
            on_done=kw["clip"],
        )
    ),
    "select <node>": Function(lambda **kw: vscode2.select_node(kw['node'], "up"))
}

extras = [
    Choice("clip", vscode_utils.clip),
    Choice("node", node_map),
    Choice("snippets", snippets),
]
utils.load_commands(contexts.python & contexts.vscode, commands=commands, extras=extras)
