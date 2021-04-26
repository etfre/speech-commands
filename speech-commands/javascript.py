from dragonfly import *
import srabuilder.actions
from srabuilder import rules

functions = {
    "console [dot] log": "console.log",
    "length": "length",
    "slice": "slice",
}

values = {
    "array": "[]",
    "object": "{}",
    "true": "true",
    "false": "false",
    "null": "null",
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
    "while loop": srabuilder.actions.type_and_move("while () {}", left=1)
    + srabuilder.actions.between(Key("enter"), Key("up"), Key("end"), Key("left:3")),
    "for loop": srabuilder.actions.type_and_move("for (let x of ) {}", left=1)
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
    "await": "await ",
    "a sink": "async ",
    "new": "new ",
    "new scope": "{{}}{left}{enter}",
    "new function": "function () {{}}{left}{enter}{up}{end}{left:5}",
    "new method": srabuilder.actions.type_and_move("def (self and m):", left=2),
    "new class": "class  {{}}{left}{enter}{up}{home}{left:6}",
    "else if [statement]": "else if () {{}}{left}{enter}{up}{end}{left:3}",
    "else [statement]": "else {{}}{left}{enter}",
    "new class": "class  {{}}{left}{enter}{up}{home}{left:6}",
    "<functions>": Text("%(functions)s"),
    "call <functions>": Text("%(functions)s()"),
    "<values>": Text("%(values)s"),
}
def rule_builder():
    builder = rules.RuleBuilder()
    extras = [Choice("functions", functions), Choice("values", values)]
    builder.basic.append(rules.ParsedRule(mapping=mapping, extras=extras))
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
