from dragonfly import *
from srabuilder import rules

functions = {
    "all": "all",
    "any": "any",
    "enumerate": "enumerate",
    "eye d": "id",
    "float": "float",
    "input": "input",
    "int": "int",
    "join": "join",
    "length": "len",
    "list": "list",
    "min": "min",
    "max": "max",
    "print": "print",
    "range": "range",
    "reversed": "reversed",
    "slice": "slice",
    "sorted": "sorted",
    "split": "split",
    "string": "str",
    "sum": "sum",
    "super": "super",
    "update": "update",
    "oh ess [dot] path [dot] join": "os.path.join"
}

errors = {
    "(assert|assertion) error": "AssertionError",
    "key error": "KeyError",
    "exception": "Exception",
    "import error": "ImportError",
    "index error": "IndexError",
    "not implemented error": "NotImplementedError",
    "oh s error": "OSError",
    "run time error": "RuntimeError",
    "type error": "TypeError",
    "value error": "ValueError",
}

mapping = {
    "import": Text("import "),
    "assign": Text(" = "),
    "compare": Text(" == "),
    "list comprehension": "[x for x in ]{left}",
    "from": Text("from "),
    "assert": Text("assert "),
    "return": Text("return "),
    "break": Text("break"),
    "continue": Text("continue"),
    "in": Text(" in "),
    "is": Text(" is "),
    "not": Text(" not "),
    "and": Text(" and "),
    "or": Text(" or "),
    "<errors>": "%(errors)s",
    "if statement": "if :{left}",
    "while loop": "while :{left}",
    "else statement": "else:{enter}",
    "if else": "if :\npass\nelse:\npass{up:3}{left}",
    "else if statement": "elif :{left}",
    "try except": "try:{c-enter}pass{c-enter}except:{c-enter}pass{up:2}{c-d}",
    "pass": "pass",
    "true": "True",
    "false": "False",
    "none": "None",
    "dictionary": "{{}}{left}",
    "slice": "[:]{left:2}",
    "new function": "def ():{left:3}",
    "new method": "def (self):{left:7}",
    "new class": "class :{enter}def __init__(self):{enter}pass{up:2}{end}{left}",
    "function <functions>": "%(functions)s",
    "call <functions>": "%(functions)s(){left}",
    "read file": "with open() as f:{left:7}",
    "write file": "with open(, 'w') as f:{left:12}",
    "read binary": "with open(, 'rb') as f:{left:14}",
    "write binary": "with open(, 'wb') as f:{left:14}",
    "with statement": "with :{left}",
    "with as": "with  as :{left:5}",
    "for loop": "for :{left}",
    "for enumerate": "for i,  in enumerate():{left:16}",
    "string index": '[""]{left:2}',
}

def rule_builder():
    builder = rules.RuleBuilder()
    extras = [Choice("functions", functions), Choice("errors", errors)]
    builder.basic.append(rules.ParsedRule(mapping=mapping, extras=extras))
    return builder
