from dragonfly import *
import srabuilder.actions
from srabuilder import rules

functions = {
    "console [dot] log": "console.log",
    "length": "length",
    "slice": "slice",
    "set timeout": "setTimeout",
    "set interval": "setInterval",
    "fetch": "fetch",
    "get element by id": "getElementById",
    "sort": "sorted",
    "has own property": "hasOwnProperty",
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
    "switch statement":"switch () {{}}{left}{enter}{up}{end}{left:3}",
    "case statement": "case :{left}",
    "assign": " = ",
    "double compare": " == ",
    "compare": " === ",
    "not": "!",
    "and": " && ",
    "or": " || ",
    "true": "true",
    "false": "false",
    "null": "null",
    "undefined": "undefined",
    "document": "document",
    "await": "await ",
    "a sink": "async ",
    "new": "new ",
    "return": "return ",
    "break": "break",
    "continue": "continue",
    "new scope": "{{}}{left}{enter}",
    "new function": "function () {{}}{left}{enter}{up}{end}{left:4}",
    "new arrow function": "() => ",
    "new method": srabuilder.actions.type_and_move("def (self and m):", left=2),
    "new class": "class  {{}}{left}{enter}{up}{home}{left:6}",
    "function <functions>": "%(functions)s",
    "call <functions>": "%(functions)s(){left}",
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
    extras = [Choice("functions", functions)]
    builder.basic.append(rules.ParsedRule(mapping=mapping, extras=extras))
    return builder
