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
    "slice": "slice",
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
    "if": Text("if "),                    
    "while": Text("if "),                    
    "<errors>": Text("%(errors)s"),
    "if statement": "if :{left}",
    "if else": "if :\npass\nelse:\npass{up:3}{left}",
    "else if": "elif :{left}",
    "else statement": "else:{enter}",
    "try except": "try:{c-enter}pass{c-enter}except:{c-enter}pass{up:2}{c-d}",
    "pass": "pass",
    "true": Text("True"),
    "false": Text("False"),
    "none": Text("None"),
    "dictionary": "{{}}{left}",
    "dictionary": "{{}}{left}",
    "slice": "[:]{left:2}",
    "new function": "def ():{left:3}",
    "new method": "def (self):{left:7}",
    "new class": "class :{left}",
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
    "while loop": "while :{left}",
    "string index": '[""]{left:2}',
}

def rule_builder():
    builder = rules.RuleBuilder()
    extras = [Choice("functions", functions), Choice("errors", errors)]
    builder.basic.append(rules.ParsedRule(mapping=mapping, extras=extras))
    return builder
