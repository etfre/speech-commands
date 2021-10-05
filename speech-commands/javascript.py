from dragonfly import *
import srabuilder.actions
from srabuilder import rules

import utils
import contexts


functions = {
    "console [dot] log": "console.log",
    "length": "length",
    "slice": "slice",
    "set timeout": "setTimeout",
    "set interval": "setInterval",
    "fetch": "fetch",
    "get element by id": "getElementById",
    "sort": "sort",
    "has own property": "hasOwnProperty",
    "use state": "useState",
    "use effect": "useEffect",
}

mapping = {
    "let": "let ",
    "const": "const ",
    "if statement":"if () {{}}{left}{enter}{up}{end}{left:3}",
    "while loop":"while () {{}}{left}{enter}{up}{end}{left:3}",
    "for loop":"for (const x of ) {{}}{left}{enter}{up}{end}{left:3}",
    "for range":"for (let i = 0; i < ; i++) {{}}{left}{enter}{up}{end}{left:8}",
    "else if [statement]": "else if () {{}}{left}{enter}{up}{end}{left:3}",
    "else statement": "else {{}}{left}{enter}",
    "switch statement":"switch () {{}}{left}{enter}{up}{end}{left:3}",
    "case statement": "case :{left}",
    "assign": " = ",
    "double compare": " == ",
    "compare": " === ",
    "say not": "!",
    "say and": " && ",
    "say or": " || ",
    "true": "true",
    "false": "false",
    "null": "null",
    "undefined": "undefined",
    "document": "document",
    "await": "await ",
    "a sink": "async ",
    "new statement": "new ",
    "return": "return ",
    "break": "break",
    "continue": "continue",
    "new scope": "{{}}{left}{enter}",
    "new function": "function () {{}}{left}{enter}{up}{end}{left:4}",
    "new arrow function": "() => ",
    "new method": "() {{}}{left}{enter}{up}{end}{left:4}",
    "new class": "class  {{}}{left}{enter}constructor() {{}}{left}{enter}{up:2}{end}{left:2}",
    "name <functions>": "%(functions)s",
    "call <functions>": "%(functions)s(){left}",
    "array": "[]{left}",
    "object": "{{}}{left}",
    "true": "true",
    "false": "false",
    "null": "null",
    "string": "''{left}",
    "double string": '""{left}',
    "template string": '``{left}',
    "export": "export ",
    "default": "default ",
    "interface": "interface ",
    "constructor": "constructor",
    "type": "type ",
    "key of": "keyof ",
    "annotate": ": ",
    "name number": "number",
    "name string": "string",
    "implements": "implements ",
    "extends": "extends ",
    "generic": "<>{left}",
    "import statement": 'import  from "";{left:9}',
    "import": 'import ',
}

extras = [Choice("functions", functions)]
utils.load_commands(contexts.javascript, commands=mapping, extras=extras)
