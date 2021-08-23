from dragonfly import *
import srabuilder.actions
from srabuilder import rules

functions = {
    "console [dot] log": "console.log",
    "length": "length",
    "slice": "slice",
}

values = {

}

mapping = {
    "let": "let ",
    "const": "const ",
    "if statement":"if () {{}}{left}{enter}{up}{end}{left:3}",
    "while loop":"while () {{}}{left}{enter}{up}{end}{left:3}",
    "for loop":"for (const x of ) {{}}{left}{enter}{up}{end}{left:3}",
    "for range":"for (let i = 0; i < ; i++) {{}}{left}{enter}{up}{end}{left:8}",
    "else if statement": "else if () {{}}{left}{enter}{up}{end}{left:3}",
    "else statement": "else {{}}{left}{enter}",
    "assign": " = ",
    "double compare": " == ",
    "compare": " === ",
    "not": "!",
    "and": " && ",
    "or": " || ",
    "true": "true",
    "false": "false",
    "null": "null",
    "await": "await ",
    "a sink": "async ",
    "new": "new ",
    "return": "return ",
    "new scope": "{{}}{left}{enter}",
    "new function": "function () {{}}{left}{enter}{up}{end}{left:4}",
    "new arrow function": "() => ",
    "new method": srabuilder.actions.type_and_move("def (self and m):", left=2),
    "new class": "class  {{}}{left}{enter}{up}{home}{left:6}",
    "function <functions>": "%(functions)s",
    "call <functions>": "%(functions)s()",
    "array": "[]{left}",
    "object": "{{}}{left}",
    "true": "true",
    "false": "false",
    "null": "null",
    "string": "''{left}",
    "double string": '""{left}',
    "template string": '``{left}',
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
