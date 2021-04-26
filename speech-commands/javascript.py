from dragonfly import *
import srabuilder.actions
from srabuilder import rules

functions = {
    "all": "all",
    "any": "any",
    "eye d": "id",
    "float": "float",
    "input": "input",
    "int": "int",
    "join": "join",
    "length": "len",
    "list": "list",
    "min": "min",
    "max": "max",
    "slice": "slice",
    "split": "split",
    "string": "str",
    "sum": "sum",
    "super": "super",
    "update": "update",
}

values = {
    "list": "[]",
    "dictionary": "{}",
    "true": "True",
    "false": "False",
    "none": "None",
}


def withScope(text):
    srabuilder.actions.type_and_move("if () {}", left=1) + srabuilder.actions.between(
        Key("enter"), Key("up"), Key("end"), Key("left:3")
    )


mapping = {
    "let": Text("let "),
    "const": Text("const "),
    "if statement": srabuilder.actions.type_and_move("if () {}", left=1)
    + srabuilder.actions.between(Key("enter"), Key("up"), Key("end"), Key("left:3")),
    "while statement": srabuilder.actions.type_and_move("while () {}", left=1)
    + srabuilder.actions.between(Key("enter"), Key("up"), Key("end"), Key("left:3")),
    "for statement": srabuilder.actions.type_and_move("for (let x of ) {}", left=1)
    + srabuilder.actions.between(Key("enter"), Key("up"), Key("end"), Key("left:3")),
    "assign": Text(" = "),
    "compare": Text("=="),
    "triple compare": Text("==="),
    "not": Text("!"),
    "and": Text(" && "),
    "or": Text(" || "),
    "true": Text("true"),
    "false": Text("false"),
    "null": Text("null"),
    "slice": srabuilder.actions.type_and_move("[:]", left=2),
    "new function": srabuilder.actions.type_and_move("def ():", left=2),
    "new method": srabuilder.actions.type_and_move("def (self and m):", left=2),
    "new class": srabuilder.actions.type_and_move("class :", left=1),
    "<functions>": Text("%(functions)s"),
    "call <functions>": Text("%(functions)s()"),
    "hatch <values>": Text(" = %(values)s") + Key("home"),
    "read file": srabuilder.actions.type_and_move("with open() as f:", left=7),
    "write file": srabuilder.actions.type_and_move("with open(, 'w') as f:", left=12),
    "read binary": srabuilder.actions.type_and_move("with open(, 'rb') as f:", left=14),
    "write binary": srabuilder.actions.type_and_move(
        "with open(, 'wb') as f:", left=14
    ),
}


def rule_builder():
    builder = rules.RuleBuilder()
    extras = [Choice("functions", functions), Choice("values", values)]
    builder.basic.append(MappingRule(mapping=mapping, extras=extras, exported=False))
    return builder


# class PythonRule(MappingRule):
#     mapping = {
#         "import ":  Text(' import '),
#     }
#     extras = [ ]
#     export=True
#     context=AppContext(title='visual studio')

# grammar.add_rule(PythonRule())
# grammar.load()
